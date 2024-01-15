import asyncio
from datetime import datetime
from typing import Dict, List


class PacketOrderer:
    """Class which orders the synchronization packets."""

    def __init__(self, out_of_order_listener, ordering_timeout_in_seconds: float):
        """Initializes the class.

        Args:
            out_of_order_listener: A function which will receive out of order packet events.
            ordering_timeout_in_seconds: Packet ordering timeout.
        """
        self._out_of_order_listener = out_of_order_listener
        self._ordering_timeout_in_seconds = ordering_timeout_in_seconds
        self._is_out_of_order_emitted = {}
        self._wait_list_size_limit = 100
        self._out_of_order_interval = None
        self._sequence_number_by_instance = {}
        self._last_session_start_timestamp = {}
        self._packets_by_instance = {}

    def start(self):
        """Initializes the packet orderer"""
        self._sequence_number_by_instance = {}
        self._last_session_start_timestamp = {}
        self._packets_by_instance = {}

        if not self._out_of_order_interval:

            async def emit_events():
                while True:
                    await asyncio.sleep(1)
                    self._emit_out_of_order_events()

            self._out_of_order_interval = asyncio.create_task(emit_events())

    def stop(self):
        """Deinitializes the packet orderer."""
        if self._out_of_order_interval is not None:
            self._out_of_order_interval.cancel()
            self._out_of_order_interval = None

    def restore_order(self, packet: Dict) -> List[Dict]:
        """Processes the packet and resolves in the order of packet sequence number.

        Args:
            packet: Packet to process.

        Returns:
            Ordered packets when the packets are ready to be processed in order.
        """
        instance_id = packet["accountId"] + ":" + str(packet.get("instanceIndex", 0)) + ":" + packet.get("host", "0")
        if "sequenceNumber" not in packet:
            return [packet]
        sequence_timestamp = packet.get("sequenceTimestamp")
        if (
            packet["type"] == "synchronizationStarted"
            and packet.get("synchronizationId")
            and (
                not self._last_session_start_timestamp.get(instance_id)
                or (
                    sequence_timestamp is not None
                    and self._last_session_start_timestamp[instance_id] < sequence_timestamp
                )
            )
        ):
            # synchronization packet sequence just started
            self._is_out_of_order_emitted[instance_id] = False
            self._sequence_number_by_instance[instance_id] = packet["sequenceNumber"]
            self._last_session_start_timestamp[instance_id] = sequence_timestamp
            self._packets_by_instance[instance_id] = list(
                filter(
                    lambda wait_packet: sequence_timestamp is not None
                    and wait_packet["packet"]["sequenceTimestamp"] >= sequence_timestamp,
                    self._packets_by_instance.get(instance_id, []),
                )
            )
            return [packet] + self._find_next_packets_from_wait_list(instance_id)
        elif (
            instance_id in self._last_session_start_timestamp
            and sequence_timestamp is not None
            and sequence_timestamp < self._last_session_start_timestamp[instance_id]
        ):
            # filter out previous packets
            return []
        elif (
            instance_id in self._sequence_number_by_instance
            and packet["sequenceNumber"] == self._sequence_number_by_instance[instance_id]
        ):
            # let the duplicate s/n packet to pass through
            return [packet]
        elif (
            instance_id in self._sequence_number_by_instance
            and packet["sequenceNumber"] == self._sequence_number_by_instance[instance_id] + 1
        ):
            # in-order packet was received
            self._sequence_number_by_instance[instance_id] += 1
            self._last_session_start_timestamp[instance_id] = (
                packet["sequenceTimestamp"]
                if "sequenceTimestamp" in packet
                else self._last_session_start_timestamp[instance_id]
            )
            return [packet] + self._find_next_packets_from_wait_list(instance_id)
        else:
            # out-of-order packet was received, add it to the wait list
            self._packets_by_instance[instance_id] = self._packets_by_instance.get(instance_id, [])
            wait_list = self._packets_by_instance[instance_id]
            wait_list.append(
                {
                    "instanceId": instance_id,
                    "accountId": packet["accountId"],
                    "instanceIndex": packet.get("instanceIndex", 0),
                    "sequenceNumber": packet["sequenceNumber"],
                    "packet": packet,
                    "receivedAt": datetime.now(),
                }
            )
            wait_list.sort(key=lambda i: i["sequenceNumber"])
            while len(wait_list) > self._wait_list_size_limit:
                wait_list.pop(0)
            return []

    def on_stream_closed(self, instance_id: str):
        """Resets state for instance id.

        Args:
            instance_id: Instance id to reset state for.
        """
        if instance_id in self._packets_by_instance.keys():
            del self._packets_by_instance[instance_id]
        if instance_id in self._last_session_start_timestamp.keys():
            del self._last_session_start_timestamp[instance_id]
        if instance_id in self._sequence_number_by_instance.keys():
            del self._sequence_number_by_instance[instance_id]

    def on_reconnected(self, reconnect_account_ids: List[str]):
        """Resets state for specified accounts on reconnect.

        Args:
            reconnect_account_ids: Reconnected account ids.
        """
        for instance_id in list(self._packets_by_instance.keys()):
            if self._get_account_id_from_instance(instance_id) in reconnect_account_ids:
                del self._packets_by_instance[instance_id]
        for instance_id in list(self._last_session_start_timestamp.keys()):
            if self._get_account_id_from_instance(instance_id) in reconnect_account_ids:
                del self._last_session_start_timestamp[instance_id]
        for instance_id in list(self._sequence_number_by_instance.keys()):
            if self._get_account_id_from_instance(instance_id) in reconnect_account_ids:
                del self._sequence_number_by_instance[instance_id]

    def _get_account_id_from_instance(self, instance_id: str) -> str:
        return instance_id.split(":")[0]

    def _find_next_packets_from_wait_list(self, instance_id) -> List:
        result = []
        wait_list = self._packets_by_instance.get(instance_id, [])
        while len(wait_list) and (
            wait_list[0]["sequenceNumber"]
            in [self._sequence_number_by_instance[instance_id], self._sequence_number_by_instance[instance_id] + 1]
            or wait_list[0]["packet"]["sequenceTimestamp"] < self._last_session_start_timestamp[instance_id]
        ):
            if wait_list[0]["packet"]["sequenceTimestamp"] >= self._last_session_start_timestamp[instance_id]:
                result.append(wait_list[0]["packet"])
                if wait_list[0]["packet"]["sequenceNumber"] == self._sequence_number_by_instance[instance_id] + 1:
                    self._sequence_number_by_instance[instance_id] += 1
                    self._last_session_start_timestamp[instance_id] = (
                        wait_list[0]["packet"]["sequenceTimestamp"]
                        if "sequenceTimestamp" in wait_list[0]["packet"]
                        else self._last_session_start_timestamp[instance_id]
                    )
            wait_list.pop(0)
        if not len(wait_list) and instance_id in self._packets_by_instance:
            del self._packets_by_instance[instance_id]
        return result

    def _emit_out_of_order_events(self):
        for key, wait_list in self._packets_by_instance.items():
            if (
                len(wait_list)
                and (wait_list[0]["receivedAt"].timestamp() + self._ordering_timeout_in_seconds)
                < datetime.now().timestamp()
            ):
                instance_id = wait_list[0]["instanceId"]
                if instance_id not in self._is_out_of_order_emitted or not self._is_out_of_order_emitted[instance_id]:
                    self._is_out_of_order_emitted[instance_id] = True
                    # Do not emit onOutOfOrderPacket for packets that come before synchronizationStarted
                    if instance_id in self._sequence_number_by_instance:
                        asyncio.create_task(
                            self._out_of_order_listener.on_out_of_order_packet(
                                wait_list[0]["accountId"],
                                wait_list[0]["instanceIndex"],
                                self._sequence_number_by_instance[instance_id] + 1,
                                wait_list[0]["sequenceNumber"],
                                wait_list[0]["packet"],
                                wait_list[0]["receivedAt"],
                            )
                        )
