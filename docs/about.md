# About

Voltarium is a modern, asynchronous Python client designed specifically for interacting with the CCEE (Brazilian Electric Energy Commercialization Chamber) API. Built with Python 3.13+, it provides developers with a clean, type-safe, and performant interface for managing energy sector operations in Brazil.

## Architecture & Design

### Modern Python Foundation

Voltarium is built on the latest Python features and best practices:

- **Python 3.13+**: Leverages the latest language features and performance improvements
- **Async/Await**: Native asynchronous programming for high-performance I/O operations
- **Type Safety**: Complete type hints throughout the codebase
- **Modern Tooling**: Uses UV for dependency management and Ruff for linting

### Clean API Design

The client follows modern Python API design principles:

```python
# Context manager support
async with VoltariumClient(...) as client:
    # All operations are async
    migration = await client.create_migration(...)

    # Automatic pagination with async generators
    async for migration in client.list_migrations(...):
        process_migration(migration)
```

## Key Features

### 🔐 Authentication & Security

Voltarium handles OAuth2 authentication automatically with robust token management:

- **Automatic Token Refresh**: Tokens are refreshed automatically before expiry
- **Retry Logic**: Failed authentication attempts are retried with exponential backoff
- **Secure Storage**: Tokens are stored securely in memory during the session
- **Error Handling**: Comprehensive authentication error handling

```python
# Authentication is handled automatically
async with VoltariumClient(
    base_url="https://api.ccee.org.br",
    client_id="your_client_id",
    client_secret="your_client_secret"
) as client:
    # All subsequent requests are automatically authenticated
    result = await client.get_migration(...)
```

### 🚀 Asynchronous Operations

Built from the ground up with async/await for maximum performance:

- **Non-blocking I/O**: All HTTP operations are asynchronous
- **Concurrent Requests**: Handle multiple operations simultaneously
- **Streaming Support**: Efficient handling of large datasets with async generators
- **Resource Management**: Proper cleanup with async context managers

```python
# Concurrent operations
async def process_multiple_migrations():
    async with VoltariumClient(...) as client:
        # These operations run concurrently
        tasks = [
            client.get_migration(agent_code="123", profile_code="456", migration_id="1"),
            client.get_migration(agent_code="123", profile_code="456", migration_id="2"),
            client.get_migration(agent_code="123", profile_code="456", migration_id="3"),
        ]

        results = await asyncio.gather(*tasks)
        return results
```

### 🛡️ Robust Error Handling

Comprehensive exception hierarchy for different error scenarios:

- **Specific Exceptions**: Different exception types for different error conditions
- **Structured Error Information**: Detailed error messages with context
- **Automatic Retry**: Configurable retry logic for transient failures
- **Status Code Mapping**: HTTP status codes mapped to appropriate exceptions

```python
from voltarium.exceptions import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError
)

try:
    migration = await client.create_migration(...)
except AuthenticationError:
    # Handle authentication issues
    print("Invalid credentials")
except ValidationError as e:
    # Handle validation errors
    print(f"Invalid data: {e.message}")
except RateLimitError:
    # Handle rate limiting
    print("Rate limit exceeded, try again later")
except NotFoundError:
    # Handle missing resources
    print("Resource not found")
except ServerError as e:
    # Handle server errors
    print(f"Server error: {e.status_code}")
```

### 🔍 Type Safety & Validation

Complete type safety with runtime validation:

- **Pydantic Models**: All data structures are validated using Pydantic
- **Type Hints**: Complete type hints throughout the codebase
- **Runtime Validation**: Input validation with detailed error messages
- **IDE Support**: Full autocomplete and type checking in modern IDEs

```python
from voltarium import CreateMigrationRequest

# Type-safe model creation
request = CreateMigrationRequest(
    consumer_unit_code="12345",
    utility_agent_code=123,
    document_type="CNPJ",  # Only valid values accepted
    document_number="12345678901234",
    retailer_agent_code=456,
    reference_month="2024-01",  # Validated format
    denunciation_date="2024-01-15",
    retailer_profile_code=789,
    consumer_unit_email="test@example.com",
    comment="Optional comment"
)

# Automatic validation
try:
    migration = await client.create_migration(request, agent_code="123", profile_code="456")
except ValidationError as e:
    print(f"Invalid data: {e.message}")
```

### 🔄 Automatic Pagination

Efficient handling of paginated results:

- **Async Generators**: Stream results as they're available
- **Automatic Page Handling**: Pagination is handled transparently
- **Memory Efficient**: Process large datasets without loading everything into memory
- **Configurable**: Control pagination behavior as needed

```python
# Automatically handles pagination
async for migration in client.list_migrations(
    initial_reference_month="2024-01",
    final_reference_month="2024-12",
    agent_code="12345",
    profile_code="67890"
):
    # Process each migration as it's retrieved
    print(f"Processing migration {migration.migration_id}")

    # Can break early if needed
    if some_condition:
        break
```

### 🧪 Comprehensive Testing

Built with testing in mind:

- **Unit Tests**: Complete test coverage for all functionality
- **Integration Tests**: Real API integration tests
- **Mocking Support**: Easy to mock for testing your own code
- **Test Factories**: Factory classes for generating test data

```python
# Easy to test your own code
import pytest
from unittest.mock import AsyncMock
from voltarium import VoltariumClient

@pytest.mark.asyncio
async def test_my_function():
    # Mock the client
    mock_client = AsyncMock(spec=VoltariumClient)
    mock_client.get_migration.return_value = MigrationItem(...)

    # Test your function
    result = await my_function(mock_client)
    assert result == expected_result
```

### 🏗️ Staging Environment with Real Data

Voltarium provides **60+ real CCEE credentials** for comprehensive testing:

- **30+ Retailer Credentials**: Working agent codes and profiles
- **30+ Utility Company Credentials**: Ready-to-use staging data
- **Real API Integration**: Test with actual CCEE staging environment

```python
from voltarium.sandbox import RETAILERS, UTILITIES

# Use real staging credentials
retailer = RETAILERS[0]
async with VoltariumClient(
    base_url="https://staging.ccee.org.br",
    client_id=retailer.client_id,
    client_secret=retailer.client_secret
) as client:
    # All operations work with real data
    migrations = client.list_migrations(...)
```

Perfect for development, testing, and integration. [Learn more about staging →](staging.md)

## Performance Characteristics

### HTTP Client

- **HTTP/2 Support**: Leverages httpx for modern HTTP support
- **Connection Pooling**: Efficient connection reuse
- **Configurable Timeouts**: Control request timeout behavior
- **Automatic Redirects**: Handles redirects transparently

### Memory Management

- **Streaming**: Large datasets are processed as streams
- **Context Managers**: Automatic resource cleanup
- **Connection Lifecycle**: Proper connection management
- **Memory Efficient**: Minimal memory footprint

### Concurrency

- **Async/Await**: Native async support
- **Concurrent Operations**: Multiple operations can run simultaneously
- **Rate Limiting**: Respect API rate limits
- **Backoff Strategies**: Intelligent retry behavior

## Next Steps

Ready to start using Voltarium? Check out:

- [**Supported Endpoints**](endpoints.md) - See all available API operations
- [**Examples**](examples.md) - Practical usage examples
- [**Staging Environment**](staging.md) - Real data testing & roadmap
