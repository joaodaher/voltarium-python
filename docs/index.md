# Voltarium Python Client

**Voltarium** is a modern, asynchronous Python client for the CCEE (Brazilian Electric Energy Commercialization Chamber) API. Built with Python 3.13+, it provides a clean, type-safe interface for interacting with CCEE services.

## Key Features

- **🚀 Asynchronous**: Built with `httpx` and `asyncio` for high performance
- **🔒 Type Safe**: Full type hints with Pydantic models
- **🛡️ Robust**: Automatic token management with retry logic
- **⚡ Modern**: Python 3.13+ with UV for dependency management
- **🏗️ Real Staging Data**: 30+ retailer and utility credentials for testing
- **✅ Well Tested**: Comprehensive integration tests with pytest

## Quick Start

Install Voltarium using your preferred package manager:

=== "UV (Recommended)"
    ```bash
    uv add voltarium
    ```

=== "pip"
    ```bash
    pip install voltarium
    ```

Then start using the client:

```python
import asyncio
from voltarium import VoltariumClient

async def main():
    async with VoltariumClient(
        base_url="https://api.ccee.org.br",
        client_id="your_client_id",
        client_secret="your_client_secret"
    ) as client:
        # List retailer migrations
        migrations = client.list_migrations(
            initial_reference_month="2024-01",
            final_reference_month="2024-12",
            agent_code="12345",
            profile_code="67890"
        )

        async for migration in migrations:
            print(f"Migration {migration.migration_id}: {migration.migration_status}")

asyncio.run(main())
```

## Getting Started

Ready to dive in? Check out our comprehensive guides:

- [**About**](about.md) - Learn about Voltarium's features and architecture
- [**Supported Endpoints**](endpoints.md) - Explore all available API endpoints
- [**Examples**](examples.md) - See practical usage examples
- [**Staging Environment**](staging.md) - Real data testing & roadmap


## Project Status

Voltarium is currently in **alpha** development. The API is stabilizing but may change between versions. We recommend pinning to specific versions in production environments.

## License

Licensed under the Apache License 2.0. See [LICENSE](https://github.com/joaodaher/voltarium-python/blob/main/LICENSE.md) for details.
