from collections.abc import AsyncGenerator

import pytest

from voltarium.client import SANDBOX_BASE_URL, VoltariumClient
from voltarium.sandbox import RETAILERS, UTILITIES, SandboxAgentCredentials


@pytest.fixture()
def retailer() -> SandboxAgentCredentials:
    return RETAILERS[0]


@pytest.fixture()
def utility() -> SandboxAgentCredentials:
    return UTILITIES[0]


@pytest.fixture()
async def client(retailer: SandboxAgentCredentials) -> AsyncGenerator[VoltariumClient]:
    client = VoltariumClient(
        base_url=SANDBOX_BASE_URL,
        client_id=retailer.client_id,
        client_secret=retailer.client_secret,
    )
    try:
        yield client
    finally:
        await client.__aexit__(None, None, None)
