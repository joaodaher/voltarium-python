# Voltarium

[![CI](https://github.com/joaodaher/voltarium-python/actions/workflows/ci.yml/badge.svg)](https://github.com/joaodaher/voltarium-python/actions/workflows/ci.yml)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**Voltarium** is an asynchronous Python 3.13 client for the CCEE (Brazilian Electric Energy Commercialization Chamber) API. Built with modern Python practices, it provides a clean, type-safe interface for interacting with CCEE services.

## 🚀 Features

- **Asynchronous**: Built with `httpx` and `asyncio` for high performance
- **Type Safe**: Full type hints with Pydantic models
- **Robust**: Automatic token management with retry logic using Tenacity
- **Modern**: Python 3.13+ with UV for dependency management
- **Well Tested**: Comprehensive test suite with pytest

## 📦 Installation

### Using UV (Recommended)

```bash
uv add voltarium
```

### Using pip

```bash
pip install voltarium
```

## 🔧 Development Setup

This project uses UV for dependency management, Task for running commands, and Ruff for linting/formatting.

```bash
# Clone the repository
git clone https://github.com/joaodaher/voltarium-python.git
cd voltarium-python

# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
task install-dev

# Run tests
task test

# Lint and format
task lint
task format

# Type checking
task mypy
```

## 🚀 Quick Start

```python
import asyncio
from voltarium import VoltariumClient

async def main():
    async with VoltariumClient(
        base_url="https://api.ccee.org.br",
        client_id="your_client_id",
        client_secret="your_client_secret"
    ) as client:
        # Perform a health check
        health = await client.health_check()
        print(f"API Status: {health['status']}")

asyncio.run(main())
```

## 📖 Documentation

### Authentication

Voltarium handles OAuth2 authentication automatically:

```python
from voltarium.auth import AuthClient

async with AuthClient(
    base_url="https://api.ccee.org.br",
    client_id="your_client_id",
    client_secret="your_client_secret"
) as auth:
    # Token is automatically managed
    headers = await auth.get_auth_header()
    print(headers)  # {'Authorization': 'Bearer <token>'}
```

### Error Handling

Voltarium provides specific exception types:

```python
from voltarium.exceptions import (
    VoltariumError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError
)

try:
    async with VoltariumClient(...) as client:
        result = await client.health_check()
except AuthenticationError:
    print("Invalid credentials")
except NotFoundError:
    print("Resource not found")
except RateLimitError:
    print("Rate limit exceeded")
except VoltariumError as e:
    print(f"API error: {e.message}")
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
task test

# Run with coverage
task test-cov

# Run specific test file
uv run pytest tests/test_auth.py -v
```

## 🛠️ Available Task Commands

```bash
task --list         # Show all available commands
task install        # Install production dependencies
task install-dev    # Install development dependencies
task test           # Run tests
task test-cov       # Run tests with coverage
task lint           # Run linting
task format         # Format code
task mypy           # Run type checking
task clean          # Clean build artifacts
task build          # Build package
task all            # Run all quality checks
task ci             # Run CI pipeline tasks
```

## 📋 Project Status

This project is in **alpha** development. The API may change between versions.

### Planned Features

- [ ] Full CCEE API endpoint coverage
- [ ] Migration endpoints (`migracoes`)
- [ ] Data validation models
- [ ] Comprehensive documentation
- [ ] Usage examples and tutorials

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 Acknowledgments

- Inspired by [PyGithub](https://github.com/pygithub/PyGithub) for client design patterns
- Built with [gcp-pilot](https://github.com/flamingo-run/gcp-pilot) project structure inspiration
- Uses [Astral UV](https://github.com/astral-sh/uv) for fast dependency management
- Code quality with [Ruff](https://github.com/astral-sh/ruff)
