import time

import pytest

from voltarium.client import VoltariumClient
from voltarium.exceptions import AuthenticationError


async def test_get_access_token_success(client) -> None:
    token_value = await client._get_access_token()

    assert isinstance(token_value, str)
    assert len(token_value) > 0

    token = client._token
    assert token is not None
    assert token.access_token == token_value
    assert token.expires_at > time.time()


async def test_get_access_token_invalid_credentials(client) -> None:
    async with VoltariumClient(
        base_url=client.base_url,
        client_id="invalid_client",
        client_secret="invalid_secret",
    ) as bad_client:
        with pytest.raises(AuthenticationError):
            await bad_client._get_access_token()


async def test_token_caching(client) -> None:
    # First call
    token_a = await client._get_access_token()

    # Second call should return the same cached token
    token_b = await client._get_access_token()

    assert token_a == token_b
