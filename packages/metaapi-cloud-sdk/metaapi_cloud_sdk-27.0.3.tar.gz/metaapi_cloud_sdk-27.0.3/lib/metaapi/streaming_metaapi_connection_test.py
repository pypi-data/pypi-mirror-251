import asyncio
from asyncio import sleep
from datetime import datetime
from typing import Coroutine, List, Dict

import pytest
from mock import MagicMock, AsyncMock, patch, ANY

from .connection_registry_model import ConnectionRegistryModel
from .history_storage import HistoryStorage
from .metatrader_account import MetatraderAccount
from .metatrader_account_replica import MetatraderAccountReplica
from .models import (
    MetatraderHistoryOrders,
    MetatraderDeals,
    MetatraderSymbolSpecification,
    MetatraderPosition,
    MetatraderOrder,
    MarketDataSubscription,
    MarketDataUnsubscription,
    MetatraderSymbolPrice,
    MetatraderTradeResponse,
    GetAccountInformationOptions,
    GetPositionsOptions,
    GetPositionOptions,
    GetOrdersOptions,
    GetOrderOptions,
    MetatraderAccountInformation,
)
from .models import date
from .streaming_metaapi_connection import StreamingMetaApiConnection
from .terminal_hash_manager import TerminalHashManager
from ..clients.error_handler import NotFoundException
from ..clients.metaapi.metaapi_websocket_client import MetaApiWebsocketClient
from ..clients.metaapi.reconnect_listener import ReconnectListener
from ..clients.metaapi.synchronization_listener import SynchronizationListener


class MockClient(MetaApiWebsocketClient):
    def get_account_information(
        self, account_id: str, options: GetAccountInformationOptions = None
    ) -> 'asyncio.Future[MetatraderAccountInformation]':
        pass

    def on_account_deleted(self, account_id: str):
        pass

    def update_account_cache(self, account_id: str, replicas: Dict):
        pass

    def get_positions(
        self, account_id: str, options: GetPositionsOptions = None
    ) -> 'asyncio.Future[List[MetatraderPosition]]':
        pass

    def get_position(
        self, account_id: str, position_id: str, options: GetPositionOptions = None
    ) -> 'asyncio.Future[MetatraderPosition]':
        pass

    def get_orders(self, account_id: str, options: GetOrdersOptions = None) -> 'asyncio.Future[List[MetatraderOrder]]':
        pass

    def get_order(
        self, account_id: str, order_id: str, options: GetOrderOptions = None
    ) -> 'asyncio.Future[MetatraderOrder]':
        pass

    def get_history_orders_by_ticket(self, account_id: str, ticket: str) -> MetatraderHistoryOrders:
        pass

    def get_history_orders_by_position(self, account_id: str, position_id: str) -> MetatraderHistoryOrders:
        pass

    def get_history_orders_by_time_range(
        self, account_id: str, start_time: datetime, end_time: datetime, offset=0, limit=1000
    ) -> MetatraderHistoryOrders:
        pass

    def get_deals_by_ticket(self, account_id: str, ticket: str) -> MetatraderDeals:
        pass

    def get_deals_by_position(self, account_id: str, position_id: str) -> MetatraderDeals:
        pass

    def get_deals_by_time_range(
        self, account_id: str, start_time: datetime, end_time: datetime, offset: int = 0, limit: int = 1000
    ) -> MetatraderDeals:
        pass

    def remove_history(self, account_id: str, application: str = None) -> Coroutine:
        pass

    def trade(
        self, account_id: str, trade, application: str = None, reliability: str = None
    ) -> 'asyncio.Future[MetatraderTradeResponse]':
        pass

    def reconnect(self, account_id: str):
        pass

    async def synchronize(
        self,
        account_id: str,
        instance_number: int,
        host: str,
        synchronization_id: str,
        starting_history_order_time: datetime,
        starting_deal_time: datetime,
        hashes,
    ) -> Coroutine:
        pass

    def subscribe(self, account_id: str, instance_index: str = None):
        pass

    async def subscribe_to_market_data(
        self, account_id: str, symbol: str, subscriptions: List[MarketDataSubscription] = None, reliability: str = None
    ) -> Coroutine:
        pass

    async def unsubscribe_from_market_data(
        self,
        account_id: str,
        symbol: str,
        subscriptions: List[MarketDataUnsubscription] = None,
        reliability: str = None,
    ) -> Coroutine:
        pass

    def add_synchronization_listener(self, account_id: str, listener):
        pass

    def add_reconnect_listener(self, listener: ReconnectListener, account_id: str):
        pass

    def remove_synchronization_listener(self, account_id: str, listener: SynchronizationListener):
        pass

    def get_symbol_specification(self, account_id: str, symbol: str) -> asyncio.Future:
        pass

    async def get_symbol_price(
        self, account_id: str, symbol: str, keep_subscription: bool = False
    ) -> 'asyncio.Future[MetatraderSymbolPrice]':
        pass

    async def wait_synchronized(
        self,
        account_id: str,
        instance_number: int,
        application_pattern: str,
        timeout_in_seconds: float,
        application: str = None,
    ):
        pass


class MockAccountReplica(MetatraderAccountReplica):
    def __init__(self, id: str, region: str):
        super().__init__(MagicMock(), MagicMock(), MagicMock())
        self._id = id
        self._region = region

    @property
    def id(self) -> str:
        return self._id

    @property
    def region(self) -> str:
        return self._region


account_replicas: List[MockAccountReplica] = None

account_regions: Dict = None


class MockAccount(MetatraderAccount):
    def __init__(self, data, metatrader_account_client, meta_api_websocket_client, connection_registry, application):
        super(MockAccount, self).__init__(
            data,
            metatrader_account_client,
            meta_api_websocket_client,
            connection_registry,
            MagicMock(),
            MagicMock(),
            application,
        )
        self._state = 'DEPLOYED'

    @property
    def id(self):
        return 'accountId'

    @property
    def synchronization_mode(self):
        return 'user'

    @property
    def state(self):
        return self._state

    @property
    def reliability(self) -> str:
        return 'regular'

    async def reload(self):
        pass

    @property
    def region(self) -> str:
        return 'vint-hill'

    @property
    def account_regions(self) -> dict:
        return account_regions

    @property
    def replicas(self) -> List[MetatraderAccountReplica]:
        return account_replicas


class MockTerminalHashManager(TerminalHashManager):
    async def refresh_ignored_field_lists(self, region: str):
        pass

    def get_specifications_by_hash(self, specification_hash: str) -> Dict[str, MetatraderSymbolSpecification]:
        pass

    def get_positions_by_hash(self, positions_hash: str) -> Dict[str, MetatraderPosition]:
        pass

    def get_orders_by_hash(self, orders_hash: str) -> Dict[str, MetatraderOrder]:
        pass

    def record_specifications(
        self,
        server_name: str,
        account_type: str,
        connection_id: str,
        instance_index: str,
        specifications: List[MetatraderSymbolSpecification],
    ) -> str:
        pass

    def record_orders(
        self, account_id: str, account_type: str, connection_id: str, instance_index: str, orders: List[MetatraderOrder]
    ) -> str:
        pass

    def update_orders(
        self,
        account_id: str,
        account_type: str,
        connection_id: str,
        instance_index: str,
        orders: List[MetatraderOrder],
        completed_orders: List[str],
        parent_hash: str,
    ) -> str:
        pass

    def get_last_used_order_hashes(self, account_id: str) -> List[str]:
        pass

    def get_last_used_position_hashes(self, account_id: str) -> List[str]:
        pass

    def get_last_used_specification_hashes(self, server_name: str) -> List[str]:
        pass


storage: HistoryStorage = None
account: MockAccount = None
client: MockClient = None
terminal_hash_manager: MockTerminalHashManager = None
api: StreamingMetaApiConnection = None
connection_registry: ConnectionRegistryModel = None
options = {'region': None}


@pytest.fixture(autouse=True)
async def run_around_tests():
    global account
    account = MockAccount(MagicMock(), MagicMock(), MagicMock(), MagicMock(), 'MetaApi')
    global account_regions
    account_regions = {'vint-hill': 'accountId', 'new-york': 'accountIdReplica'}
    global account_replicas
    account_replicas = [
        MockAccountReplica('accountIdReplica', 'new-york'),
        MockAccountReplica('replica-singapore', 'singapore'),
        MockAccountReplica('replica-tokyo', 'tokyo'),
    ]
    global client
    client = MockClient(MagicMock(), MagicMock(), 'token')
    client.get_url_settings = AsyncMock()
    client.ensure_subscribe = MagicMock()
    client.subscribe = AsyncMock()
    global storage
    storage = MagicMock()
    storage.initialize = AsyncMock()
    storage.last_history_order_time = AsyncMock(return_value=datetime.now())
    storage.last_deal_time = AsyncMock(return_value=datetime.now())
    storage.on_history_order_added = AsyncMock()
    storage.on_deal_added = AsyncMock()
    global terminal_hash_manager
    terminal_hash_manager = TerminalHashManager(AsyncMock())
    global connection_registry
    connection_registry = MagicMock()
    connection_registry.connect_streaming = MagicMock()
    connection_registry.remove_streaming = AsyncMock()
    global api
    api = StreamingMetaApiConnection(options, client, terminal_hash_manager, account, storage, connection_registry)
    api.terminal_state.specification = MagicMock(return_value={'symbol': 'EURUSD'})
    yield
    api.health_monitor.stop()


class TestStreamingMetaApiConnection:
    @pytest.mark.asyncio
    async def test_remove_application(self):
        """Should remove application."""
        await api.connect('instanceId')
        client.remove_application = AsyncMock()
        api.history_storage.clear = AsyncMock()
        await api.remove_application()
        api.history_storage.clear.assert_called()
        client.remove_application.assert_called_with('accountId')

    @pytest.mark.asyncio
    async def test_subscribe_to_terminal(self):
        """Should subscribe to terminal."""
        await api.connect('instanceId')
        await api.subscribe()
        client.ensure_subscribe.assert_any_call('accountId', 0)
        client.ensure_subscribe.assert_any_call('accountId', 1)
        client.ensure_subscribe.assert_any_call('accountIdReplica', 0)
        client.ensure_subscribe.assert_any_call('accountIdReplica', 1)

    @pytest.mark.asyncio
    async def test_not_subscribe_if_not_open(self):
        """Should not subscribe if connection is not open."""
        try:
            await api.subscribe()
            pytest.fail()
        except Exception as err:
            assert (
                err.args[0]
                == 'This connection has not been initialized yet, please invoke await ' + 'connection.connect()'
            )
        client.ensure_subscribe.assert_not_called()

    @pytest.mark.asyncio
    async def test_not_subscribe_if_closed(self):
        """Should not subscribe if connection is closed."""
        await api.connect('instanceId')
        client.ensure_subscribe = AsyncMock()
        client.unsubscribe = AsyncMock()
        await api.close('instanceId')
        try:
            await api.subscribe()
            pytest.fail()
        except Exception as err:
            assert err.args[0] == 'This connection has been closed, please create a new connection'
        client.ensure_subscribe.assert_not_called()

    @pytest.mark.asyncio
    async def test_synchronize_state_with_terminal(self):
        """Should synchronize state with terminal."""
        client.synchronize = AsyncMock()
        with patch('lib.metaapi.streaming_metaapi_connection.random_id', return_value='synchronizationId'):
            api = StreamingMetaApiConnection(options, client, terminal_hash_manager, account, None, MagicMock())
            await api.connect('instanceId')
            await api.history_storage.on_history_order_added(
                'vint-hill:1:ps-mpa-1',
                {
                    'id': '1',
                    'type': 'ORDER_TYPE_SELL',
                    'state': 'ORDER_STATE_FILLED',
                    'doneTime': date('2020-01-01T00:00:00.000Z'),
                },
            )
            await api.history_storage.on_deal_added(
                'vint-hill:1:ps-mpa-1',
                {
                    'id': '1',
                    'type': 'DEAL_TYPE_SELL',
                    'entryType': 'DEAL_ENTRY_IN',
                    'time': date('2020-01-02T00:00:00.000Z'),
                },
            )
            await api.synchronize('vint-hill:1:ps-mpa-1')
            client.synchronize.assert_called_with(
                'accountId',
                1,
                'ps-mpa-1',
                'synchronizationId',
                date('2020-01-01T00:00:00.000Z'),
                date('2020-01-02T00:00:00.000Z'),
                ANY,
            )

    @pytest.mark.asyncio
    async def test_synchronize_state_with_terminal_from_time(self):
        """Should synchronize state with terminal from specified time."""
        client.synchronize = AsyncMock()
        with patch('lib.metaapi.streaming_metaapi_connection.random_id', return_value='synchronizationId'):
            api = StreamingMetaApiConnection(
                options, client, terminal_hash_manager, account, None, MagicMock(), date('2020-10-07T00:00:00.000Z')
            )
            await api.connect('instanceId')
            await api.history_storage.on_history_order_added(
                'vint-hill:1:ps-mpa-1',
                {
                    'id': '1',
                    'type': 'ORDER_TYPE_SELL',
                    'state': 'ORDER_STATE_FILLED',
                    'doneTime': date('2020-01-01T00:00:00.000Z'),
                },
            )
            await api.history_storage.on_deal_added(
                'vint-hill:1:ps-mpa-1',
                {
                    'id': '1',
                    'type': 'DEAL_TYPE_SELL',
                    'entryType': 'DEAL_ENTRY_IN',
                    'time': date('2020-01-02T00:00:00.000Z'),
                },
            )
            await api.synchronize('vint-hill:1:ps-mpa-1')
            client.synchronize.assert_called_with(
                'accountId',
                1,
                'ps-mpa-1',
                'synchronizationId',
                date('2020-10-07T00:00:00.000Z'),
                date('2020-10-07T00:00:00.000Z'),
                ANY,
            )

    @pytest.mark.asyncio
    async def test_subscribe_to_market_data(self):
        """Should subscribe to market data."""
        await api.connect('instanceId')
        client.subscribe_to_market_data = AsyncMock()
        promise = asyncio.create_task(api.subscribe_to_market_data('EURUSD', None))
        api.terminal_state.wait_for_price = AsyncMock(
            return_value={'time': datetime.fromtimestamp(1000000), 'symbol': 'EURUSD', 'bid': 1, 'ask': 1.1}
        )
        await promise
        assert 'EURUSD' in api.subscribed_symbols
        client.subscribe_to_market_data.assert_called_with('accountId', 'EURUSD', [{'type': 'quotes'}], 'regular')
        assert api.subscriptions('EURUSD') == [{'type': 'quotes'}]
        await api.subscribe_to_market_data('EURUSD', [{'type': 'books'}, {'type': 'candles', 'timeframe': '1m'}])
        assert api.subscriptions('EURUSD') == [
            {'type': 'quotes'},
            {'type': 'books'},
            {'type': 'candles', 'timeframe': '1m'},
        ]
        await api.subscribe_to_market_data('EURUSD', [{'type': 'quotes'}, {'type': 'candles', 'timeframe': '5m'}])
        assert api.subscriptions('EURUSD') == [
            {'type': 'quotes'},
            {'type': 'books'},
            {'type': 'candles', 'timeframe': '1m'},
            {'type': 'candles', 'timeframe': '5m'},
        ]

    @pytest.mark.asyncio
    async def test_not_subscribe_if_no_specification(self):
        """Should not subscribe to symbol that has no specification"""
        await api.connect('instanceId')
        client.subscribe_to_market_data = AsyncMock()
        api.terminal_state.wait_for_price = AsyncMock(
            return_value={'time': datetime.fromtimestamp(1000000), 'symbol': 'EURUSD', 'bid': 1, 'ask': 1.1}
        )
        await api.subscribe_to_market_data('EURUSD', None, 1)
        client.subscribe_to_market_data.assert_called_with('accountId', 'EURUSD', [{'type': 'quotes'}], 'regular')
        api.terminal_state.specification = MagicMock(return_value=None)
        try:
            await api.subscribe_to_market_data('AAAAA', None, 1)
            raise Exception('ValidationException expected')
        except Exception as err:
            assert err.__class__.__name__ == 'ValidationException'

    @pytest.mark.asyncio
    async def test_unsubscribe_from_market_data(self):
        """Should unsubscribe from market data."""
        await api.connect('instanceId')
        client.subscribe_to_market_data = AsyncMock()
        client.unsubscribe_from_market_data = AsyncMock()
        api.terminal_state.wait_for_price = AsyncMock(
            return_value={'time': datetime.fromtimestamp(1000000), 'symbol': 'EURUSD', 'bid': 1, 'ask': 1.1}
        )
        await api.subscribe_to_market_data('EURUSD', [{'type': 'quotes'}])
        assert 'EURUSD' in api.subscribed_symbols
        await api.unsubscribe_from_market_data('EURUSD', [{'type': 'quotes'}])
        assert 'EURUSD' not in api.subscribed_symbols
        client.unsubscribe_from_market_data.assert_called_with('accountId', 'EURUSD', [{'type': 'quotes'}], 'regular')
        assert api.subscriptions('EURUSD') is None

        await api.subscribe_to_market_data(
            'EURUSD',
            [
                {'type': 'quotes'},
                {'type': 'books'},
                {'type': 'candles', 'timeframe': '1m'},
                {'type': 'candles', 'timeframe': '5m'},
                {'type': 'candles', 'timeframe': '15m'},
            ],
            1,
        )
        assert api.subscriptions('EURUSD') == [
            {'type': 'quotes'},
            {'type': 'books'},
            {'type': 'candles', 'timeframe': '1m'},
            {'type': 'candles', 'timeframe': '5m'},
            {'type': 'candles', 'timeframe': '15m'},
        ]

        await api.unsubscribe_from_market_data('EURUSD', [{'type': 'quotes'}, {'type': 'candles', 'timeframe': '5m'}])
        assert api.subscriptions('EURUSD') == [
            {'type': 'books'},
            {'type': 'candles', 'timeframe': '1m'},
            {'type': 'candles', 'timeframe': '15m'},
        ]

    @pytest.mark.asyncio
    async def test_unsubscribe_during_subscription_downgrade(self):
        """Should unsubscribe during market data subscription downgrade."""
        await api.connect('instanceId')
        api.subscribe_to_market_data = AsyncMock()
        api.unsubscribe_from_market_data = AsyncMock()
        await api.on_subscription_downgraded(
            'vint-hill:1:ps-mpa-1', 'EURUSD', None, [{'type': 'ticks'}, {'type': 'books'}]
        )
        api.unsubscribe_from_market_data.assert_called_with('EURUSD', [{'type': 'ticks'}, {'type': 'books'}])
        api.subscribe_to_market_data.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_market_data_subscription_on_downgrade(self):
        """Should update market data subscription on downgrade."""
        await api.connect('instanceId')
        api.subscribe_to_market_data = AsyncMock()
        api.unsubscribe_from_market_data = AsyncMock()
        await api.on_subscription_downgraded(
            'vint-hill:1:ps-mpa-1', 'EURUSD', [{'type': 'quotes', 'intervalInMilliseconds': 30000}]
        )
        api.subscribe_to_market_data.assert_called_with('EURUSD', [{'type': 'quotes', 'intervalInMilliseconds': 30000}])
        api.unsubscribe_from_market_data.assert_not_called()

    @pytest.mark.asyncio
    async def test_initialize(self):
        """Should initialize listeners, terminal state and history storage for accounts with user sync mode."""
        client.add_synchronization_listener = MagicMock()
        api = StreamingMetaApiConnection(options, client, terminal_hash_manager, account, storage, MagicMock())
        await api.connect('instanceId')
        assert api.terminal_state
        assert api.history_storage
        client.add_synchronization_listener.assert_any_call('accountId', api)
        client.add_synchronization_listener.assert_any_call('accountId', api.terminal_state)
        client.add_synchronization_listener.assert_any_call('accountId', api.history_storage)

    @pytest.mark.asyncio
    async def test_sync_on_connection(self):
        """Should synchronize on connection."""
        with patch('lib.metaapi.streaming_metaapi_connection.random_id', return_value='synchronizationId'):
            client.synchronize = AsyncMock()
            terminal_hash_manager.refresh_ignored_field_lists = AsyncMock()
            api = StreamingMetaApiConnection(options, client, terminal_hash_manager, account, storage, MagicMock())
            storage.last_history_order_time = AsyncMock(return_value=date('2020-01-01T00:00:00.000Z'))
            storage.last_deal_time = AsyncMock(return_value=date('2020-01-02T00:00:00.000Z'))
            await api.connect('instanceId')
            await api.on_connected('vint-hill:1:ps-mpa-1', 1)
            await asyncio.sleep(0.05)
            client.synchronize.assert_called_with(
                'accountId',
                1,
                'ps-mpa-1',
                'synchronizationId',
                date('2020-01-01T00:00:00.000Z'),
                date('2020-01-02T00:00:00.000Z'),
                ANY,
            )
            terminal_hash_manager.refresh_ignored_field_lists.assert_called_with('vint-hill')

    @pytest.mark.asyncio
    async def test_maintain_sync(self):
        """Should maintain synchronization if connection has failed."""
        with patch('lib.metaapi.streaming_metaapi_connection.random_id', return_value='synchronizationId'):
            client.synchronize = AsyncMock(side_effect=[Exception('test error'), None])
            api = StreamingMetaApiConnection(options, client, terminal_hash_manager, account, storage, MagicMock())
            await api.connect('instanceId')
            storage.last_history_order_time = AsyncMock(return_value=date('2020-01-01T00:00:00.000Z'))
            storage.last_deal_time = AsyncMock(return_value=date('2020-01-02T00:00:00.000Z'))
            await api.on_connected('vint-hill:1:ps-mpa-1', 1)
            await asyncio.sleep(0.05)
            client.synchronize.assert_called_with(
                'accountId',
                1,
                'ps-mpa-1',
                'synchronizationId',
                date('2020-01-01T00:00:00.000Z'),
                date('2020-01-02T00:00:00.000Z'),
                ANY,
            )

    @pytest.mark.asyncio
    async def test_not_sync_if_connection_closed(self):
        """Should not synchronize if connection is closed."""
        with patch('lib.metaapi.streaming_metaapi_connection.random_id', return_value='synchronizationId'):
            client.synchronize = AsyncMock()
            client.unsubscribe = AsyncMock()
            api = StreamingMetaApiConnection(
                options, client, terminal_hash_manager, account, storage, connection_registry
            )
            await api.connect('instanceId')
            await api.history_storage.on_history_order_added(
                'vint-hill:1:ps-mpa-1', {'doneTime': date('2020-01-01T00:00:00.000Z')}
            )
            await api.history_storage.on_deal_added('vint-hill:1:ps-mpa-1', {'time': date('2020-01-02T00:00:00.000Z')})
            await api.close('instanceId')
            await api.on_connected('vint-hill:1:ps-mpa-1', 1)
            client.synchronize.assert_not_called()

    @pytest.mark.asyncio
    async def test_unsubscribe_from_events_on_close(self):
        """Should unsubscribe from events on close."""
        client.add_synchronization_listener = MagicMock()
        client.remove_synchronization_listener = MagicMock()
        client.unsubscribe = AsyncMock()
        api = StreamingMetaApiConnection(options, client, terminal_hash_manager, account, storage, connection_registry)
        api._terminal_state.close = MagicMock()
        await api.connect('instanceId')
        await api.close('instanceId')
        client.remove_synchronization_listener.assert_any_call('accountId', api)
        client.remove_synchronization_listener.assert_any_call('accountId', api.terminal_state)
        client.remove_synchronization_listener.assert_any_call('accountId', api.history_storage)
        connection_registry.remove_streaming.assert_called_with(account)
        api._terminal_state.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_connection_if_all_instances_closed(self):
        """Should close connection only if all instances closed."""
        client.add_synchronization_listener = MagicMock()
        client.remove_synchronization_listener = MagicMock()
        api = StreamingMetaApiConnection(options, client, terminal_hash_manager, account, storage, connection_registry)
        await api.connect('accountId')
        await api.connect('accountId')
        await api.connect('accountId2')
        await api.connect('accountId3')
        await api.close('accountId')
        client.remove_synchronization_listener.assert_not_called()
        await api.close('accountId3')
        client.remove_synchronization_listener.assert_not_called()
        await api.close('accountId2')
        client.remove_synchronization_listener.assert_any_call('accountId', api)
        client.remove_synchronization_listener.assert_any_call('accountId', api.terminal_state)
        client.remove_synchronization_listener.assert_any_call('accountId', api.history_storage)
        connection_registry.remove_streaming.assert_called_with(account)

    @pytest.mark.asyncio
    async def test_close_connection_if_all_instances_closed(self):
        """Should close connection only if all instances closed."""
        client.add_synchronization_listener = MagicMock()
        client.remove_synchronization_listener = MagicMock()
        api = StreamingMetaApiConnection(options, client, terminal_hash_manager, account, storage, connection_registry)
        await api.close('accountId')
        client.remove_synchronization_listener.assert_not_called()
        await api.connect('accountId')
        await api.close('accountId')
        client.remove_synchronization_listener.assert_any_call('accountId', api)
        client.remove_synchronization_listener.assert_any_call('accountId', api.terminal_state)
        client.remove_synchronization_listener.assert_any_call('accountId', api.history_storage)
        connection_registry.remove_streaming.assert_called_with(account)

    @pytest.mark.asyncio
    async def test_wait_sync_complete_user_mode(self):
        """Should wait until synchronization complete."""
        client.wait_synchronized = AsyncMock()
        await api.connect('instanceId')
        assert not (await api.is_synchronized('vint-hill:1:ps-mpa-1'))
        api._history_storage.update_disk_storage = AsyncMock()
        try:
            await api.wait_synchronized(
                {
                    'applicationPattern': 'app.*',
                    'synchronizationId': 'synchronizationId',
                    'timeoutInSeconds': 1,
                    'intervalInMilliseconds': 10,
                }
            )
            raise Exception('TimeoutError is expected')
        except Exception as err:
            assert err.__class__.__name__ == 'TimeoutException'
        await api.on_history_orders_synchronized('vint-hill:1:ps-mpa-1', 'synchronizationId')
        await api.on_deals_synchronized('vint-hill:1:ps-mpa-1', 'synchronizationId')
        promise = api.wait_synchronized(
            {
                'applicationPattern': 'app.*',
                'synchronizationId': 'synchronizationId',
                'timeoutInSeconds': 1,
                'intervalInMilliseconds': 10,
            }
        )
        start_time = datetime.now()
        await promise
        assert pytest.approx(10, 10) == (datetime.now() - start_time).seconds * 1000
        assert await api.is_synchronized('vint-hill:1:ps-mpa-1', 'synchronizationId')
        client.wait_synchronized.assert_called_with('accountId', 1, 'app.*', ANY)

    @pytest.mark.asyncio
    async def test_wait_sync_complete_replica(self):
        """Should wait synchronize on a replica."""
        client.wait_synchronized = AsyncMock()
        await api.connect('instanceId')
        assert not (await api.is_synchronized('new-york:1:ps-mpa-1'))
        api._history_storage.update_disk_storage = AsyncMock()
        try:
            await api.wait_synchronized(
                {
                    'applicationPattern': 'app.*',
                    'synchronizationId': 'synchronizationId',
                    'timeoutInSeconds': 1,
                    'intervalInMilliseconds': 10,
                }
            )
            raise Exception('TimeoutError is expected')
        except Exception as err:
            assert err.__class__.__name__ == 'TimeoutException'
        await api.on_history_orders_synchronized('new-york:1:ps-mpa-1', 'synchronizationId')
        await api.on_deals_synchronized('new-york:1:ps-mpa-1', 'synchronizationId')
        promise = api.wait_synchronized(
            {
                'applicationPattern': 'app.*',
                'synchronizationId': 'synchronizationId',
                'timeoutInSeconds': 1,
                'intervalInMilliseconds': 10,
            }
        )
        start_time = datetime.now()
        await promise
        assert pytest.approx(10, 10) == (datetime.now() - start_time).seconds * 1000
        assert await api.is_synchronized('new-york:1:ps-mpa-1', 'synchronizationId')
        client.wait_synchronized.assert_called_with('accountIdReplica', 1, 'app.*', ANY)

    @pytest.mark.asyncio
    async def test_time_out_waiting_for_sync(self):
        """Should time out waiting for synchronization complete."""
        await api.connect('instanceId')
        try:
            await api.wait_synchronized(
                {
                    'applicationPattern': 'app.*',
                    'synchronizationId': 'synchronizationId',
                    'timeoutInSeconds': 1,
                    'intervalInMilliseconds': 10,
                }
            )
            raise Exception('TimeoutError is expected')
        except Exception as err:
            assert err.__class__.__name__ == 'TimeoutException'
        assert not (await api.is_synchronized('vint-hill:1:ps-mpa-1', 'synchronizationId'))

    @pytest.mark.asyncio
    async def test_initialize_connection(self):
        """Should initialize connection."""
        client.add_account_cache = MagicMock()
        await api.connect('instanceId')
        api._history_storage.initialize = AsyncMock()
        await api.initialize()
        api._history_storage.initialize.assert_called()
        client.add_account_cache.assert_called_with(
            'accountId', {'new-york': 'accountIdReplica', 'vint-hill': 'accountId'}
        )

    @pytest.mark.asyncio
    async def test_disconnect(self):
        """Should set synchronized false on disconnect."""
        await api.connect('instanceId')
        client.synchronize = AsyncMock()
        await api.on_connected('vint-hill:1:ps-mpa-1', 2)
        await asyncio.sleep(0.05)
        assert api.synchronized
        account.reload = AsyncMock()
        await api.on_disconnected('vint-hill:1:ps-mpa-1')
        assert not api.synchronized

    @pytest.mark.asyncio
    async def test_on_stream_closed(self):
        """Should delete state if stream closed."""
        await api.connect('instanceId')
        client.synchronize = AsyncMock()
        await api.on_connected('vint-hill:1:ps-mpa-1', 2)
        await asyncio.sleep(0.05)
        assert api.synchronized
        await api.on_stream_closed('vint-hill:1:ps-mpa-1')
        assert not api.synchronized

    @pytest.mark.asyncio
    async def test_create_refresh_market_data_subscriptions_job(self):
        """Should create refresh subscriptions job."""
        with patch('lib.metaapi.streaming_metaapi_connection.asyncio.sleep', new=lambda x: sleep(x / 10)):
            with patch('lib.metaapi.streaming_metaapi_connection.uniform', new=MagicMock(return_value=1)):
                await api.connect('instanceId')
                client.refresh_market_data_subscriptions = AsyncMock()
                client.subscribe_to_market_data = AsyncMock()
                client.add_synchronization_listener = MagicMock()
                client.remove_synchronization_listener = MagicMock()
                client.unsubscribe = AsyncMock()
                api.terminal_state.wait_for_price = AsyncMock()
                await api.on_synchronization_started('vint-hill:1:ps-mpa-1')
                await sleep(0.05)
                client.refresh_market_data_subscriptions.assert_called_with('accountId', 1, [])
                await api.subscribe_to_market_data('EURUSD', [{'type': 'quotes'}], 1)
                await sleep(0.11)
                client.refresh_market_data_subscriptions.assert_called_with(
                    'accountId', 1, [{'symbol': 'EURUSD', 'subscriptions': [{'type': 'quotes'}]}]
                )
                assert client.refresh_market_data_subscriptions.call_count == 2
                await api.on_synchronization_started('vint-hill:1:ps-mpa-1')
                await sleep(0.05)
                assert client.refresh_market_data_subscriptions.call_count == 3
                await api.close('instanceId')
                await sleep(0.11)
                assert client.refresh_market_data_subscriptions.call_count == 3

    @pytest.mark.asyncio
    async def test_create_refresh_market_data_subscriptions_job_replica(self):
        """Should create refresh subscriptions job with a replica."""
        with patch('lib.metaapi.streaming_metaapi_connection.asyncio.sleep', new=lambda x: sleep(x / 10)):
            with patch('lib.metaapi.streaming_metaapi_connection.uniform', new=MagicMock(return_value=1)):
                await api.connect('instanceId')
                client.refresh_market_data_subscriptions = AsyncMock()
                client.subscribe_to_market_data = AsyncMock()
                client.add_synchronization_listener = MagicMock()
                client.remove_synchronization_listener = MagicMock()
                client.unsubscribe = AsyncMock()
                api.terminal_state.wait_for_price = AsyncMock()
                await api.on_synchronization_started('new-york:1:ps-mpa-1')
                await sleep(0.05)
                client.refresh_market_data_subscriptions.assert_called_with('accountIdReplica', 1, [])
                await api.subscribe_to_market_data('EURUSD', [{'type': 'quotes'}], 1)
                await sleep(0.11)
                client.refresh_market_data_subscriptions.assert_called_with(
                    'accountIdReplica', 1, [{'symbol': 'EURUSD', 'subscriptions': [{'type': 'quotes'}]}]
                )
                assert client.refresh_market_data_subscriptions.call_count == 2
                await api.on_synchronization_started('new-york:1:ps-mpa-1')
                await sleep(0.05)
                assert client.refresh_market_data_subscriptions.call_count == 3
                await api.close('instanceId')
                await sleep(0.11)
                assert client.refresh_market_data_subscriptions.call_count == 3

    @pytest.mark.asyncio
    async def test_remove_subscription_job_on_region_unsubscribe(self):
        """Should remove subscription job on region unsubscribe."""
        with patch('lib.metaapi.streaming_metaapi_connection.asyncio.sleep', new=lambda x: sleep(x / 10)):
            with patch('lib.metaapi.streaming_metaapi_connection.uniform', new=MagicMock(return_value=1)):
                await api.connect('instanceId')
                client.refresh_market_data_subscriptions = AsyncMock()
                client.subscribe_to_market_data = AsyncMock()
                client.add_synchronization_listener = MagicMock()
                client.remove_synchronization_listener = MagicMock()
                client.unsubscribe = AsyncMock()
                api.terminal_state.wait_for_price = AsyncMock()
                await api.on_synchronization_started('vint-hill:1:ps-mpa-1')
                await sleep(0.05)
                client.refresh_market_data_subscriptions.assert_called_with('accountId', 1, [])
                await api.subscribe_to_market_data('EURUSD', [{'type': 'quotes'}], 1)
                await sleep(0.11)
                client.refresh_market_data_subscriptions.assert_called_with(
                    'accountId', 1, [{'symbol': 'EURUSD', 'subscriptions': [{'type': 'quotes'}]}]
                )
                assert client.refresh_market_data_subscriptions.call_count == 2
                await api.on_unsubscribe_region('vint-hill')
                await sleep(0.11)
                assert client.refresh_market_data_subscriptions.call_count == 2
                await api.close('instanceId')

    @pytest.mark.asyncio
    async def test_clear_region_states_on_socket_reconnect(self):
        """Should clear region states on socket reconnect."""
        with patch('lib.metaapi.streaming_metaapi_connection.asyncio.sleep', new=lambda x: sleep(x / 10)):
            with patch('lib.metaapi.streaming_metaapi_connection.uniform', new=MagicMock(return_value=1)):
                await api.connect('instanceId')
                client.refresh_market_data_subscriptions = AsyncMock()
                client.subscribe_to_market_data = AsyncMock()
                client.add_synchronization_listener = MagicMock()
                client.remove_synchronization_listener = MagicMock()
                client.unsubscribe = AsyncMock()
                await api.on_synchronization_started('new-york:1:ps-mpa-1')
                await api.on_synchronization_started('vint-hill:1:ps-mpa-1')
                await sleep(0.05)
                client.refresh_market_data_subscriptions.assert_any_call('accountIdReplica', 1, [])
                client.refresh_market_data_subscriptions.assert_any_call('accountId', 1, [])
                await api.terminal_state.on_symbol_prices_updated(
                    'new-york:1:ps-mpa-1',
                    [
                        {
                            'time': datetime.now(),
                            'symbol': 'EURUSD',
                            'bid': 1,
                            'ask': 1.1,
                            'brokerTime': '2022-01-01 02:00:00.000',
                        }
                    ],
                )
                await api.terminal_state.on_symbol_prices_updated(
                    'vint-hill:1:ps-mpa-1',
                    [
                        {
                            'time': datetime.now(),
                            'symbol': 'EURUSD',
                            'bid': 1,
                            'ask': 1.1,
                            'brokerTime': '2022-01-01 02:00:00.000',
                        }
                    ],
                )
                await api.subscribe_to_market_data('EURUSD', [{'type': 'quotes'}], 1)
                await sleep(0.11)
                assert client.refresh_market_data_subscriptions.call_count == 4
                await api.on_reconnected('new-york', 1)
                await sleep(0.11)
                assert client.refresh_market_data_subscriptions.call_count == 5
                await api.on_reconnected('vint-hill', 1)
                await sleep(0.11)
                assert client.refresh_market_data_subscriptions.call_count == 5


class TestScheduleRefresh:
    @pytest.mark.asyncio
    async def test_close_account_on_not_found_exception(self):
        """Should close account on NotFoundException."""
        with patch('lib.metaapi.streaming_metaapi_connection.asyncio.sleep', new=lambda x: sleep(x / 21600)):
            account.reload = AsyncMock(side_effect=NotFoundException('test'))
            connection_registry.close_all_instances = MagicMock()
            api.schedule_refresh('vint-hill')
            await sleep(1)
            connection_registry.close_all_instances.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_replica_list(self):
        """Should update replica list."""
        with patch('lib.metaapi.streaming_metaapi_connection.asyncio.sleep', new=lambda x: sleep(x / 21600)):

            async def reload_account():
                global account_replicas
                account_replicas = [
                    MockAccountReplica('replica-singapore2', 'singapore'),
                    MockAccountReplica('replica-tokyo', 'tokyo'),
                    MockAccountReplica('replica-london', 'london'),
                ]
                global account_regions
                account_regions = {
                    'vint-hill': 'accountId',
                    'singapore': 'replica-singapore2',
                    'tokyo': 'replica-tokyo',
                    'london': 'replica-london',
                }

            account.reload = AsyncMock(side_effect=reload_account)
            client.on_account_deleted = MagicMock()
            client.ensure_subscribe = MagicMock()
            client.update_account_cache = MagicMock()
            api.schedule_refresh('vint-hill')
            await sleep(1)

            client.on_account_deleted.assert_any_call('accountIdReplica')
            client.on_account_deleted.assert_any_call('replica-singapore')
            client.update_account_cache.assert_any_call(
                'accountId',
                {
                    'london': 'replica-london',
                    'singapore': 'replica-singapore2',
                    'tokyo': 'replica-tokyo',
                    'vint-hill': 'accountId',
                },
            )
            client.ensure_subscribe.assert_any_call('accountId', 0)
            client.ensure_subscribe.assert_any_call('accountId', 1)
            client.ensure_subscribe.assert_any_call('replica-singapore2', 0)
            client.ensure_subscribe.assert_any_call('replica-singapore2', 1)
            client.ensure_subscribe.assert_any_call('replica-tokyo', 0)
            client.ensure_subscribe.assert_any_call('replica-tokyo', 1)
            client.ensure_subscribe.assert_any_call('replica-london', 0)
            client.ensure_subscribe.assert_any_call('replica-london', 1)
