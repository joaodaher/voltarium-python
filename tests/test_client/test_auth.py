import time

import pytest

from tests.base import SandboxTestCase
from voltarium.client import VoltariumClient
from voltarium.exceptions import AuthenticationError


class AuthClientTestCase(SandboxTestCase):
    """Integration tests for authentication."""

    async def test_get_access_token_success(self) -> None:
        """Test successful token retrieval."""
        async with self.client:
            token_value = await self.client._get_access_token()

        assert isinstance(token_value, str)
        assert len(token_value) > 0

        token = self.client._token
        assert token is not None
        assert token.access_token == token_value
        assert token.expires_at > time.time()

    async def test_get_access_token_invalid_credentials(self) -> None:
        """Test token retrieval with invalid credentials."""
        async with VoltariumClient(
            base_url=self.client.base_url,
            client_id="invalid_client",
            client_secret="invalid_secret",
        ) as client:
            with pytest.raises(AuthenticationError):
                await client._get_access_token()

    async def test_token_caching(self) -> None:
        """Test that tokens are cached properly."""
        async with self.client:
            # First call
            token_a = await self.client._get_access_token()

            # Second call should return the same cached token
            token_b = await self.client._get_access_token()

            assert token_a == token_b
