# Voltarium

[![CI](https://github.com/joaodaher/voltarium-python/actions/workflows/ci.yml/badge.svg)](https://github.com/joaodaher/voltarium-python/actions/workflows/ci.yml)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**Modern, asynchronous Python client for the CCEE (Brazilian Electric Energy Commercialization Chamber) API.** Built with Python 3.13+ and designed for high-performance energy sector applications.

## 🚀 Key Features

- **🔥 Asynchronous**: Built with `httpx` and `asyncio` for maximum performance
- **🔒 Type Safe**: Complete type hints with Pydantic models for bulletproof code
- **🛡️ Robust**: Automatic OAuth2 token management with intelligent retry logic
- **🏗️ Real Staging Data**: 60+ authentic CCEE credentials for comprehensive testing
- **⚡ Modern**: Python 3.13+ with UV for lightning-fast dependency management
- **✅ Production Ready**: Comprehensive test suite and error handling

## 📦 Installation

```bash
# Using UV (recommended)
uv add voltarium

# Using pip
pip install voltarium
```

## 🔥 Quick Start

```python
import asyncio
from voltarium import VoltariumClient

async def main():
    async with VoltariumClient(
        client_id="your_client_id",
        client_secret="your_client_secret"
    ) as client:
        # List retailer migrations with automatic pagination
        migrations = client.list_migrations(
            initial_reference_month="2024-01",
            final_reference_month="2024-12",
            agent_code="12345",
            profile_code="67890"
        )

        # Stream results efficiently
        async for migration in migrations:
            print(f"Migration {migration.migration_id}: {migration.migration_status}")

asyncio.run(main())
```

## 🏗️ Real Staging Environment

Test with **real CCEE data** using our comprehensive staging environment:

```python
from voltarium.sandbox import RETAILERS, UTILITIES
from voltarium import SANDBOX_BASE_URL

# Use real staging credentials
retailer = RETAILERS[0]  # 30+ available retailers
utility = UTILITIES[0]   # 30+ available utilities

# Test with actual CCEE staging API
async with VoltariumClient(
    base_url=SANDBOX_BASE_URL,
    client_id=retailer.client_id,
    client_secret=retailer.client_secret
) as client:
    # All operations work with real data
    migrations = await client.list_migrations(...)
```

## 📚 Comprehensive Documentation

Visit our **[complete documentation](https://voltarium.github.io/voltarium-python/)** for:

- **[About](https://voltarium.github.io/voltarium-python/about/)** - Architecture and detailed features
- **[Supported Endpoints](https://voltarium.github.io/voltarium-python/endpoints/)** - Complete API reference
- **[Examples](https://voltarium.github.io/voltarium-python/examples/)** - Practical usage patterns
- **[Staging Environment](https://voltarium.github.io/voltarium-python/staging/)** - Real data testing & roadmap

## 🛠️ Development

```bash
# Clone and setup
git clone https://github.com/joaodaher/voltarium-python.git
cd voltarium-python

# Install dependencies (requires UV)
task install-dev

# Run tests
task test

# Quality checks
task lint && task format && task typecheck
```

## 🎯 Current Status

**Alpha Release** - Core migration endpoints fully supported:

✅ **Retailer Migrations** - Complete CRUD operations
🚧 **Utility Migrations** - Under development
📋 **Additional Endpoints** - [See roadmap](https://voltarium.github.io/voltarium-python/staging/#roadmap)

## 🤝 Contributing

We welcome contributions! Please see our [documentation](https://voltarium.github.io/voltarium-python/) for details on:

- Feature roadmap and priorities
- Development setup and guidelines
- Testing with real staging data

## 📄 License

Apache License 2.0 - see [LICENSE.md](LICENSE.md) for details.

---

**Built for the Brazilian energy sector** 🇧🇷 | **Powered by modern Python** 🐍
