import pytest
from mock import MagicMock

from .http_client import HttpClient
from .metaapi_client import MetaApiClient

http_client = HttpClient()
token = 'token'
api_token = 'header.payload.sign'
api_client: MetaApiClient = None
domain_client: MagicMock = None


@pytest.fixture(autouse=True)
async def run_around_tests():
    global http_client
    http_client = HttpClient()
    global domain_client
    domain_client = MagicMock()
    domain_client.token = token
    domain_client.domain = 'agiliumtrade.agiliumtrade.ai'
    global api_client
    api_client = MetaApiClient(http_client, domain_client)
    yield


class TestMetaApiClient:
    @pytest.mark.asyncio
    async def test_return_account_token_type(self):
        """Should return account token type."""
        assert api_client._token_type == 'account'

    @pytest.mark.asyncio
    async def test_return_api_token_type(self):
        """Should return api token type."""
        domain_client.token = api_token
        api_client = MetaApiClient(http_client, domain_client)
        assert api_client._token_type == 'api'

    @pytest.mark.asyncio
    async def test_check_token_not_jwt(self):
        """Should check that current token is not JWT."""
        assert api_client._is_not_jwt_token()

    @pytest.mark.asyncio
    async def test_check_token_not_account(self):
        """Should check that current token is not account token."""
        domain_client.token = api_token
        api_client = MetaApiClient(http_client, domain_client)
        assert api_client._is_not_account_token()

    @pytest.mark.asyncio
    async def test_handle_no_access_exception_with_account_token(self):
        """Should handle no access exception with account token."""
        try:
            api_client._handle_no_access_exception('methodName')
            pytest.fail()
        except Exception as err:
            assert (
                err.__str__()
                == 'You can not invoke methodName method, because you have connected with account '
                + 'access token. Please use API access token from '
                + 'https://app.metaapi.cloud/api-access/generate-token page to invoke this method.'
            )

    @pytest.mark.asyncio
    async def test_handle_no_access_exception_with_api_token(self):
        """Should handle no access exception with api token."""
        domain_client.token = api_token
        api_client = MetaApiClient(http_client, domain_client)
        try:
            api_client._handle_no_access_exception('methodName')
            pytest.fail()
        except Exception as err:
            assert (
                err.__str__()
                == 'You can not invoke methodName method, because you have connected with API '
                + 'access token. Please use account access token to invoke this method.'
            )
