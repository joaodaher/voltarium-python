# Supported Endpoints

Voltarium currently supports the retailer migration endpoints of the CCEE API. These endpoints allow you to manage the complete lifecycle of energy retailer migrations in Brazil.

## Client Setup

### VoltariumClient

The main client class for interacting with the CCEE API.

#### Constructor

```python
def __init__(
    self,
    *,
    base_url: str,
    client_id: str,
    client_secret: str,
    timeout: float = 30.0,
    max_retries: int = 3,
) -> None:
```

**Parameters:**

- `base_url` (str): Base URL for the API
- `client_id` (str): OAuth2 client ID
- `client_secret` (str): OAuth2 client secret
- `timeout` (float, optional): Request timeout in seconds. Defaults to 30.0
- `max_retries` (int, optional): Maximum number of retries for failed requests. Defaults to 3

**Example:**
```python
client = VoltariumClient(
    base_url="https://api.ccee.org.br",
    client_id="your_client_id",
    client_secret="your_client_secret",
    timeout=60.0,
    max_retries=5
)
```

#### Context Manager

VoltariumClient supports async context management:

```python
async with VoltariumClient(...) as client:
    # Use client here
    pass
```

## Migration Endpoints (🇧🇷 Migracoes)

The migration endpoints provide full CRUD (Create, Read, Update, Delete) operations for managing retailer migrations. All endpoints are asynchronous and include automatic authentication, error handling, and retry logic.

### Overview

| Operation | Method | Endpoint | Description |
|-----------|--------|----------|-------------|
| [List Migrations](#list-migrations) | GET | `/varejistas/migracoes` | List migrations with filtering and pagination |
| [Create Migration](#create-migration) | POST | `/varejistas/migracoes` | Create a new migration |
| [Get Migration](#get-migration) | GET | `/varejistas/migracoes/{id}` | Get a specific migration by ID |
| [Update Migration](#update-migration) | PUT | `/varejistas/migracoes/{id}` | Update an existing migration |
| [Delete Migration](#delete-migration) | DELETE | `/varejistas/migracoes/{id}` | Delete a migration |

## List Migrations

Retrieve a paginated list of migrations with optional filtering.

### Usage

```python
async with VoltariumClient(...) as client:
    # Get all migrations for a date range
    migrations = client.list_migrations(
        initial_reference_month="2024-01",
        final_reference_month="2024-12",
        agent_code="12345",
        profile_code="67890"
    )

    # Process each migration
    async for migration in migrations:
        print(f"Migration {migration.migration_id}: {migration.migration_status}")
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `initial_reference_month` | `str` | Yes | Start reference month (YYYY-MM format) |
| `final_reference_month` | `str` | Yes | End reference month (YYYY-MM format) |
| `agent_code` | `str` | Yes | Agent code for the request |
| `profile_code` | `str` | Yes | Profile code for the request |
| `consumer_unit_code` | `str` | No | Filter by consumer unit code |
| `migration_status` | `str` | No | Filter by migration status |

### Response

Returns an async generator of `MigrationListItem` objects with the following fields:

```python
class MigrationListItem:
    migration_id: str
    consumer_unit_code: str
    utility_agent_consumer_unit_code: str
    utility_agent_code: int
    document_type: str
    document_number: str
    retailer_agent_code: int
    request_date: datetime
    retailer_profile_code: int
    migration_status: str
    submarket: str | None
    dhc_value: float | None
    musd_value: float | None
    penalty_payment: str | None
    justification: str | None
    validation_date: datetime | None
    consumer_unit_email: str
    comment: str | None
    supplier_agent_code: int | None
    reference_month: datetime
    denunciation_date: datetime
    cer_celebration_id: str | None
```

### Example

```python
async def list_all_migrations():
    async with VoltariumClient(...) as client:
        # List migrations with filtering
        migrations = client.list_migrations(
            initial_reference_month="2024-01",
            final_reference_month="2024-03",
            agent_code="12345",
            profile_code="67890",
            consumer_unit_code="UC123456",  # Optional filter
            migration_status="PENDING"      # Optional filter
        )

        migration_list = []
        async for migration in migrations:
            migration_list.append(migration)
            print(f"Found migration: {migration.migration_id}")

        print(f"Total migrations found: {len(migration_list)}")
        return migration_list
```

## Create Migration

Create a new retailer migration.

### Usage

```python
from voltarium import CreateMigrationRequest

async with VoltariumClient(...) as client:
    # Create a migration request
    request = CreateMigrationRequest(
        consumer_unit_code="12345",
        utility_agent_code=123,
        document_type="CNPJ",
        document_number="12345678901234",
        retailer_agent_code=456,
        reference_month="2024-01",
        denunciation_date="2024-01-15",
        retailer_profile_code=789,
        consumer_unit_email="contact@example.com",
        comment="Migration request comment"
    )

    # Create the migration
    migration = await client.create_migration(
        migration_data=request,
        agent_code="12345",
        profile_code="67890"
    )

    print(f"Created migration: {migration.migration_id}")
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `migration_data` | `CreateMigrationRequest` | Yes | Migration data object |
| `agent_code` | `str` | Yes | Agent code for the request |
| `profile_code` | `str` | Yes | Profile code for the request |

### CreateMigrationRequest Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `consumer_unit_code` | `str` | Yes | Consumer unit code |
| `utility_agent_code` | `int \| str` | Yes | Utility agent code |
| `document_type` | `Literal["CNPJ"]` | Yes | Document type (only CNPJ supported) |
| `document_number` | `str` | Yes | Document number (will be validated) |
| `retailer_agent_code` | `int \| str` | Yes | Retailer agent code |
| `reference_month` | `str` | Yes | Reference month (YYYY-MM format) |
| `denunciation_date` | `str` | Yes | Denunciation date (YYYY-MM-DD format) |
| `retailer_profile_code` | `int \| str` | Yes | Retailer profile code |
| `consumer_unit_email` | `str` | Yes | Consumer unit email |
| `comment` | `str` | No | Optional comment |

### Response

Returns a `MigrationItem` object with the created migration details.

### Example

```python
async def create_migration():
    async with VoltariumClient(...) as client:
        try:
            request = CreateMigrationRequest(
                consumer_unit_code="UC123456",
                utility_agent_code=100,
                document_type="CNPJ",
                document_number="12.345.678/0001-90",  # Will be automatically cleaned
                retailer_agent_code=200,
                reference_month="2024-06",
                denunciation_date="2024-06-15",
                retailer_profile_code=300,
                consumer_unit_email="billing@company.com",
                comment="Quarterly migration request"
            )

            migration = await client.create_migration(
                migration_data=request,
                agent_code="12345",
                profile_code="67890"
            )

            print(f"✅ Migration created successfully!")
            print(f"   ID: {migration.migration_id}")
            print(f"   Status: {migration.migration_status}")
            print(f"   Request Date: {migration.request_date}")

            return migration

        except ValidationError as e:
            print(f"❌ Validation error: {e.message}")
        except AuthenticationError:
            print("❌ Authentication failed")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
```

## Get Migration

Retrieve a specific migration by its ID.

### Usage

```python
async with VoltariumClient(...) as client:
    migration = await client.get_migration(
        migration_id="MIGRATION_ID_123",
        agent_code="12345",
        profile_code="67890"
    )

    print(f"Migration status: {migration.migration_status}")
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `migration_id` | `str` | Yes | Unique migration ID |
| `agent_code` | `str` | Yes | Agent code for the request |
| `profile_code` | `str` | Yes | Profile code for the request |

### Response

Returns a `MigrationItem` object with detailed migration information.

### Example

```python
async def get_migration_details(migration_id: str):
    async with VoltariumClient(...) as client:
        try:
            migration = await client.get_migration(
                migration_id=migration_id,
                agent_code="12345",
                profile_code="67890"
            )

            print(f"📋 Migration Details:")
            print(f"   ID: {migration.migration_id}")
            print(f"   Status: {migration.migration_status}")
            print(f"   Consumer Unit: {migration.consumer_unit_code}")
            print(f"   Email: {migration.consumer_unit_email}")
            print(f"   Request Date: {migration.request_date}")

            if migration.validation_date:
                print(f"   Validation Date: {migration.validation_date}")

            if migration.comment:
                print(f"   Comment: {migration.comment}")

            return migration

        except NotFoundError:
            print(f"❌ Migration {migration_id} not found")
        except AuthenticationError:
            print("❌ Authentication failed")
```

## Update Migration

Update an existing migration.

### Usage

```python
from voltarium import UpdateMigrationRequest

async with VoltariumClient(...) as client:
    # Create update request
    update_request = UpdateMigrationRequest(
        reference_month="2024-02",
        retailer_profile_code=789,
        document_type="CNPJ",
        document_number="12345678901234",
        consumer_unit_email="updated@example.com"
    )

    # Update the migration
    migration = await client.update_migration(
        migration_id="MIGRATION_ID_123",
        migration_data=update_request,
        agent_code="12345",
        profile_code="67890"
    )

    print(f"Updated migration: {migration.migration_id}")
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `migration_id` | `str` | Yes | Unique migration ID |
| `migration_data` | `UpdateMigrationRequest` | Yes | Updated migration data |
| `agent_code` | `str` | Yes | Agent code for the request |
| `profile_code` | `str` | Yes | Profile code for the request |

### UpdateMigrationRequest Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `reference_month` | `str` | Yes | Reference month (YYYY-MM format) |
| `retailer_profile_code` | `int` | Yes | Retailer profile code |
| `document_type` | `Literal["CNPJ"]` | Yes | Document type (only CNPJ supported) |
| `document_number` | `str` | Yes | Document number (will be validated) |
| `consumer_unit_email` | `str` | Yes | Consumer unit email |

### Response

Returns a `MigrationItem` object with the updated migration details.

## Delete Migration

Delete an existing migration.

### Usage

```python
async with VoltariumClient(...) as client:
    await client.delete_migration(
        migration_id="MIGRATION_ID_123",
        agent_code="12345",
        profile_code="67890"
    )

    print("Migration deleted successfully")
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `migration_id` | `str` | Yes | Unique migration ID |
| `agent_code` | `str` | Yes | Agent code for the request |
| `profile_code` | `str` | Yes | Profile code for the request |

### Response

Returns `None` on successful deletion.

### Example

```python
async def delete_migration_safely(migration_id: str):
    async with VoltariumClient(...) as client:
        try:
            # First, get the migration to confirm it exists
            migration = await client.get_migration(
                migration_id=migration_id,
                agent_code="12345",
                profile_code="67890"
            )

            print(f"⚠️  About to delete migration:")
            print(f"   ID: {migration.migration_id}")
            print(f"   Status: {migration.migration_status}")
            print(f"   Consumer Unit: {migration.consumer_unit_code}")

            # Delete the migration
            await client.delete_migration(
                migration_id=migration_id,
                agent_code="12345",
                profile_code="67890"
            )

            print("✅ Migration deleted successfully")

        except NotFoundError:
            print(f"❌ Migration {migration_id} not found")
        except AuthenticationError:
            print("❌ Authentication failed")
```

## Error Handling

All endpoints include comprehensive error handling:

### Common Exceptions

- **`AuthenticationError`**: Invalid credentials or expired tokens
- **`ValidationError`**: Invalid request data or parameters
- **`NotFoundError`**: Migration or resource not found
- **`RateLimitError`**: API rate limit exceeded
- **`ServerError`**: Internal server error

### Best Practices

1. **Always use try-catch blocks** for production code
2. **Handle specific exception types** rather than generic exceptions
3. **Implement retry logic** for transient failures
4. **Log errors appropriately** for debugging

```python
from voltarium.exceptions import (
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
    ServerError
)

async def robust_migration_operation():
    async with VoltariumClient(...) as client:
        try:
            # Your migration operation here
            result = await client.create_migration(...)
            return result

        except ValidationError as e:
            logger.error(f"Validation failed: {e.message}")
            raise
        except AuthenticationError:
            logger.error("Authentication failed - check credentials")
            raise
        except NotFoundError:
            logger.warning("Resource not found")
            return None
        except RateLimitError:
            logger.warning("Rate limit exceeded - retrying later")
            await asyncio.sleep(60)  # Wait and retry
            return await robust_migration_operation()
        except ServerError as e:
            logger.error(f"Server error: {e.status_code}")
            raise
```
