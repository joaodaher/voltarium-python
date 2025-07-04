# Staging Environment

Voltarium provides real CCEE staging data for testing and development.

## What is Staging Data?

The staging environment includes **60+ real CCEE agent credentials** that work with the actual CCEE staging API:

- **30+ Retailers**: Agent codes 200000-200049 with 1-2 profile codes each
- **30+ Utilities**: Agent codes 100000-100009 and 400000-400019 with 1 profile code each
- **Real OAuth2 Credentials**: Working client IDs and secrets
- **Live API Access**: All endpoints work with real staging data

## How to Use

### Basic Usage

```python
from voltarium import VoltariumClient
from voltarium.sandbox import RETAILERS, UTILITIES

# Pick any retailer for testing
retailer = RETAILERS[0]  # Agent 200000, profiles [200100, 200101]

# Create client with real staging credentials
async with VoltariumClient(
    base_url="https://staging.ccee.org.br",
    client_id=retailer.client_id,
    client_secret=retailer.client_secret
) as client:
    # All API operations work with real data
    migrations = client.list_migrations(
        initial_reference_month="2024-01",
        final_reference_month="2024-12",
        agent_code=str(retailer.agent_code),
        profile_code=str(retailer.profiles[0])
    )

    async for migration in migrations:
        print(f"Real migration: {migration.migration_id}")
```

### Testing Different Agents

```python
# Test with different retailers
for retailer in RETAILERS[:3]:
    print(f"Retailer {retailer.agent_code}: {len(retailer.profiles)} profiles")

# Test with different utilities
for utility in UTILITIES[:3]:
    print(f"Utility {utility.agent_code}: {len(utility.profiles)} profiles")
```

### Integration Tests

```python
import pytest
from voltarium.sandbox import RETAILERS

class TestWithStagingData:
    """Integration tests using real staging data."""

    @pytest.mark.asyncio
    async def test_real_migration_flow(self):
        """Test complete migration flow with staging data."""
        retailer = RETAILERS[0]

        async with VoltariumClient(
            base_url="https://staging.ccee.org.br",
            client_id=retailer.client_id,
            client_secret=retailer.client_secret
        ) as client:
            # Test with real staging environment
            migrations = await client.list_migrations(
                initial_reference_month="2024-01",
                final_reference_month="2024-12",
                agent_code=str(retailer.agent_code),
                profile_code=str(retailer.profiles[0])
            )

            count = 0
            async for migration in migrations:
                count += 1
                assert migration.migration_id
                assert migration.agent_code == retailer.agent_code

            print(f"Found {count} real migrations")
```

## How it Works

### Data Structure

Each agent credential contains:

```python
@dataclass
class SandboxAgentCredentials:
    client_id: str        # OAuth2 client ID
    client_secret: str    # OAuth2 client secret
    agent_code: int       # CCEE agent code
    profiles: list[int]    # Available profile codes
```

### Agent Types

- **Retailers** (`RETAILERS`): Energy retailers with 2 profile codes each
- **Utilities** (`UTILITIES`): Utility companies with 1 profile code each

### Authentication

All credentials are pre-configured for OAuth2 authentication with the CCEE staging API. No additional setup required.

### Real Data

The staging environment contains real migration data that you can:

- **List**: Browse existing migrations
- **Create**: Add new test migrations
- **Update**: Modify existing migrations
- **Delete**: Remove test migrations

Perfect for integration testing, development, and API exploration without affecting production data.
