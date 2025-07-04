# Examples

This page provides practical examples of using Voltarium for common tasks. All examples include proper error handling and follow best practices.

## Basic Setup

First, let's establish the basic setup pattern used throughout these examples:

```python
import asyncio
import os
from datetime import datetime, timedelta
from voltarium import VoltariumClient, CreateMigrationRequest, UpdateMigrationRequest
from voltarium.exceptions import (
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
    ServerError
)

# Configuration
CLIENT_CONFIG = {
    "base_url": "https://api.ccee.org.br",
    "client_id": os.getenv("CCEE_CLIENT_ID"),
    "client_secret": os.getenv("CCEE_CLIENT_SECRET"),
    "timeout": 30.0,
    "max_retries": 3
}

# Common parameters
AGENT_CODE = "12345"
PROFILE_CODE = "67890"
CONCESSIONARIA_CODE = 100
```

## Simple Migration Management

### Creating a Single Migration

```python
async def create_simple_migration():
    """Create a single migration with basic error handling."""
    async with VoltariumClient(**CLIENT_CONFIG) as client:
        try:
            # Create migration request
            request = CreateMigrationRequest(
                consumer_unit_code="UC123456",
                utility_agent_code=CONCESSIONARIA_CODE,
                document_type="CNPJ",
                document_number="12345678901234",
                retailer_agent_code=AGENT_CODE,
                reference_month="2024-06",
                denunciation_date="2024-06-15",
                retailer_profile_code=PROFILE_CODE,
                consumer_unit_email="billing@company.com",
                comment="Monthly migration request"
            )

            # Create the migration
            migration = await client.create_migration(
                migration_data=request,
                agent_code=AGENT_CODE,
                profile_code=PROFILE_CODE
            )

            print(f"✅ Migration created: {migration.migration_id}")
            print(f"   Status: {migration.migration_status}")
            print(f"   Consumer Unit: {migration.consumer_unit_code}")

            return migration

        except ValidationError as e:
            print(f"❌ Validation error: {e.message}")
            return None
        except AuthenticationError:
            print("❌ Authentication failed - check credentials")
            return None

# Run the example
if __name__ == "__main__":
    asyncio.run(create_simple_migration())
```

### Retrieving Migration Details

```python
async def get_migration_example():
    """Retrieve and display migration details."""
    async with VoltariumClient(**CLIENT_CONFIG) as client:
        try:
            migration = await client.get_migration(
                migration_id="MIGRATION_ID_123",
                agent_code=AGENT_CODE,
                profile_code=PROFILE_CODE
            )

            print(f"📋 Migration Details:")
            print(f"   ID: {migration.migration_id}")
            print(f"   Status: {migration.migration_status}")
            print(f"   Consumer Unit: {migration.consumer_unit_code}")
            print(f"   Email: {migration.consumer_unit_email}")
            print(f"   Request Date: {migration.request_date}")
            print(f"   Reference Date: {migration.reference_date}")

            if migration.validation_date:
                print(f"   Validation Date: {migration.validation_date}")

            if migration.comment:
                print(f"   Comment: {migration.comment}")

            return migration

        except NotFoundError:
            print("❌ Migration not found")
            return None
        except AuthenticationError:
            print("❌ Authentication failed")
            return None

# Run the example
if __name__ == "__main__":
    asyncio.run(get_migration_example())
```

## Bulk Operations

### Creating Multiple Migrations

```python
async def create_bulk_migrations():
    """Create multiple migrations efficiently."""
    async with VoltariumClient(**CLIENT_CONFIG) as client:
        # Define migration data
        migrations_data = [
            {
                "consumer_unit_code": f"UC{i:06d}",
                "consumer_unit_email": f"billing{i}@company.com",
                "reference_month": "2024-06",
                "comment": f"Bulk migration {i}"
            }
            for i in range(1, 11)  # Create 10 migrations
        ]

        created_migrations = []
        failed_migrations = []

        for i, data in enumerate(migrations_data, 1):
            try:
                request = CreateMigrationRequest(
                    consumer_unit_code=data["consumer_unit_code"],
                    utility_agent_code=CONCESSIONARIA_CODE,
                    document_type="CNPJ",
                    document_number=f"12345678{i:06d}",
                    retailer_agent_code=AGENT_CODE,
                    reference_month=data["reference_month"],
                    denunciation_date="2024-06-15",
                    retailer_profile_code=PROFILE_CODE,
                    consumer_unit_email=data["consumer_unit_email"],
                    comment=data["comment"]
                )

                migration = await client.create_migration(
                    migration_data=request,
                    agent_code=AGENT_CODE,
                    profile_code=PROFILE_CODE
                )

                created_migrations.append(migration)
                print(f"✅ Created migration {i}: {migration.migration_id}")

            except ValidationError as e:
                failed_migrations.append({"index": i, "error": e.message})
                print(f"❌ Failed to create migration {i}: {e.message}")
            except Exception as e:
                failed_migrations.append({"index": i, "error": str(e)})
                print(f"❌ Unexpected error for migration {i}: {e}")

        print(f"\n📊 Summary:")
        print(f"   Created: {len(created_migrations)}")
        print(f"   Failed: {len(failed_migrations)}")

        return created_migrations, failed_migrations

# Run the example
if __name__ == "__main__":
    asyncio.run(create_bulk_migrations())
```

### Concurrent Operations

```python
async def concurrent_migration_operations():
    """Perform multiple operations concurrently."""
    async with VoltariumClient(**CLIENT_CONFIG) as client:
        # Migration IDs to process
        migration_ids = ["MIG_001", "MIG_002", "MIG_003", "MIG_004", "MIG_005"]

        # Create tasks for concurrent execution
        tasks = [
            client.get_migration(
                migration_id=mid,
                agent_code=AGENT_CODE,
                profile_code=PROFILE_CODE
            )
            for mid in migration_ids
        ]

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        successful = []
        failed = []

        for i, result in enumerate(results):
            migration_id = migration_ids[i]

            if isinstance(result, Exception):
                failed.append({"id": migration_id, "error": str(result)})
                print(f"❌ Failed to get {migration_id}: {result}")
            else:
                successful.append(result)
                print(f"✅ Retrieved {migration_id}: {result.migration_status}")

        print(f"\n📊 Concurrent Operations Summary:")
        print(f"   Successful: {len(successful)}")
        print(f"   Failed: {len(failed)}")

        return successful, failed

# Run the example
if __name__ == "__main__":
    asyncio.run(concurrent_migration_operations())
```

## Advanced Filtering and Pagination

### Filtering Migrations

```python
async def filter_migrations_example():
    """Demonstrate filtering migrations with different criteria."""
    async with VoltariumClient(**CLIENT_CONFIG) as client:
        # Filter by date range and status
        print("🔍 Filtering migrations...")

        filters = [
            {
                "name": "All migrations in 2024",
                "params": {
                    "initial_reference_month": "2024-01",
                    "final_reference_month": "2024-12",
                    "agent_code": AGENT_CODE,
                    "profile_code": PROFILE_CODE
                }
            },
            {
                "name": "Pending migrations",
                "params": {
                    "initial_reference_month": "2024-01",
                    "final_reference_month": "2024-12",
                    "agent_code": AGENT_CODE,
                    "profile_code": PROFILE_CODE,
                    "migration_status": "PENDING"
                }
            },
            {
                "name": "Specific consumer unit",
                "params": {
                    "initial_reference_month": "2024-01",
                    "final_reference_month": "2024-12",
                    "agent_code": AGENT_CODE,
                    "profile_code": PROFILE_CODE,
                    "consumer_unit_code": "UC123456"
                }
            }
        ]

        for filter_config in filters:
            print(f"\n📋 {filter_config['name']}:")

            try:
                migrations = client.list_migrations(**filter_config["params"])

                count = 0
                async for migration in migrations:
                    count += 1
                    print(f"   {count}. {migration.migration_id} - {migration.migration_status}")

                    # Limit output for demo
                    if count >= 5:
                        print("   ... (more results available)")
                        break

                print(f"   Total shown: {count}")

            except Exception as e:
                print(f"   ❌ Error: {e}")

# Run the example
if __name__ == "__main__":
    asyncio.run(filter_migrations_example())
```

### Processing Large Datasets

```python
async def process_large_dataset():
    """Process a large dataset of migrations efficiently."""
    async with VoltariumClient(**CLIENT_CONFIG) as client:
        # Statistics tracking
        stats = {
            "total_processed": 0,
            "status_counts": {},
            "errors": []
        }

        try:
            # Get all migrations for the year
            migrations = client.list_migrations(
                initial_reference_month="2024-01",
                final_reference_month="2024-12",
                agent_code=AGENT_CODE,
                profile_code=PROFILE_CODE
            )

            print("📊 Processing large dataset...")

            # Process migrations in batches
            batch_size = 100
            batch = []

            async for migration in migrations:
                batch.append(migration)
                stats["total_processed"] += 1

                # Track status counts
                status = migration.migration_status
                stats["status_counts"][status] = stats["status_counts"].get(status, 0) + 1

                # Process batch when full
                if len(batch) >= batch_size:
                    await process_migration_batch(batch)
                    batch = []

                    # Progress update
                    if stats["total_processed"] % 500 == 0:
                        print(f"   Processed {stats['total_processed']} migrations...")

            # Process remaining migrations
            if batch:
                await process_migration_batch(batch)

            # Print final statistics
            print(f"\n📈 Processing Complete:")
            print(f"   Total Processed: {stats['total_processed']}")
            print(f"   Status Breakdown:")
            for status, count in stats["status_counts"].items():
                print(f"     {status}: {count}")

            if stats["errors"]:
                print(f"   Errors: {len(stats['errors'])}")

        except Exception as e:
            print(f"❌ Error processing dataset: {e}")
            stats["errors"].append(str(e))

        return stats

async def process_migration_batch(batch):
    """Process a batch of migrations."""
    # Example processing logic
    for migration in batch:
        # Perform any required processing
        # This could include validation, transformation, etc.
        pass

# Run the example
if __name__ == "__main__":
    asyncio.run(process_large_dataset())
```

## Error Handling Patterns

### Comprehensive Error Handling

```python
async def robust_migration_client():
    """Demonstrate comprehensive error handling patterns."""

    async def safe_create_migration(client, request_data):
        """Create migration with comprehensive error handling."""
        max_retries = 3
        retry_delay = 1.0

        for attempt in range(max_retries):
            try:
                request = CreateMigrationRequest(**request_data)

                migration = await client.create_migration(
                    migration_data=request,
                    agent_code=AGENT_CODE,
                    profile_code=PROFILE_CODE
                )

                print(f"✅ Migration created: {migration.migration_id}")
                return migration

            except ValidationError as e:
                print(f"❌ Validation error (attempt {attempt + 1}): {e.message}")
                if attempt == max_retries - 1:
                    raise

            except AuthenticationError:
                print(f"❌ Authentication failed (attempt {attempt + 1})")
                if attempt == max_retries - 1:
                    raise

            except RateLimitError:
                print(f"⏳ Rate limit exceeded (attempt {attempt + 1}), waiting...")
                await asyncio.sleep(retry_delay * (2 ** attempt))  # Exponential backoff

            except ServerError as e:
                print(f"🔧 Server error (attempt {attempt + 1}): {e.status_code}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(retry_delay)

            except Exception as e:
                print(f"❌ Unexpected error (attempt {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(retry_delay)

        return None

    async with VoltariumClient(**CLIENT_CONFIG) as client:
        # Test data
        migration_data = {
            "consumer_unit_code": "UC123456",
            "utility_agent_code": CONCESSIONARIA_CODE,
            "document_type": "CNPJ",
            "document_number": "12345678901234",
            "retailer_agent_code": AGENT_CODE,
            "reference_month": "2024-06",
            "denunciation_date": "2024-06-15",
            "retailer_profile_code": PROFILE_CODE,
            "consumer_unit_email": "test@company.com",
            "comment": "Robust error handling test"
        }

        result = await safe_create_migration(client, migration_data)
        return result

# Run the example
if __name__ == "__main__":
    asyncio.run(robust_migration_client())
```

### Circuit Breaker Pattern

```python
class CircuitBreaker:
    """Simple circuit breaker implementation."""

    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = await func(*args, **kwargs)
            self.reset()
            return result
        except Exception as e:
            self.record_failure()
            raise

    def record_failure(self):
        """Record a failure."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

    def reset(self):
        """Reset the circuit breaker."""
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_failure_time = None

async def circuit_breaker_example():
    """Demonstrate circuit breaker pattern."""
    import time

    circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10)

    async def protected_get_migration(client, migration_id):
        """Protected migration retrieval."""
        return await circuit_breaker.call(
            client.get_migration,
            migration_id=migration_id,
            agent_code=AGENT_CODE,
            profile_code=PROFILE_CODE
        )

    async with VoltariumClient(**CLIENT_CONFIG) as client:
        # Test with invalid migration ID to trigger failures
        test_ids = ["INVALID_1", "INVALID_2", "INVALID_3", "INVALID_4"]

        for migration_id in test_ids:
            try:
                result = await protected_get_migration(client, migration_id)
                print(f"✅ Retrieved: {migration_id}")
            except Exception as e:
                print(f"❌ Failed: {migration_id} - {e}")
                print(f"   Circuit breaker state: {circuit_breaker.state}")

# Run the example
if __name__ == "__main__":
    asyncio.run(circuit_breaker_example())
```

## Testing and Mocking

### Unit Testing with Mocks

```python
import pytest
from unittest.mock import AsyncMock, patch
from voltarium import VoltariumClient, MigrationItem

class TestMigrationOperations:
    """Example unit tests for migration operations."""

    @pytest.mark.asyncio
    async def test_create_migration_success(self):
        """Test successful migration creation."""
        # Mock response
        mock_migration = MigrationItem(
            migration_id="TEST_123",
            consumer_unit_code="UC123456",
            utility_agent_consumer_unit_code="UTIL123",
            utility_agent_code=100,
            document_type="CNPJ",
            document_number="12345678901234",
            retailer_agent_code=200,
            request_date=datetime.now(),
            retailer_profile_code=300,
            migration_status="PENDING",
            consumer_unit_email="test@example.com",
            reference_date=datetime.now()
        )

        # Mock the client
        with patch('voltarium.client.VoltariumClient') as mock_client:
            mock_client_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            mock_client_instance.create_migration.return_value = mock_migration

            # Test the function
            async with VoltariumClient(**CLIENT_CONFIG) as client:
                result = await client.create_migration(
                    migration_data=CreateMigrationRequest(
                        consumer_unit_code="UC123456",
                        utility_agent_code=100,
                        document_type="CNPJ",
                        document_number="12345678901234",
                        retailer_agent_code=200,
                        reference_month="2024-06",
                        denunciation_date="2024-06-15",
                        retailer_profile_code=300,
                        consumer_unit_email="test@example.com"
                    ),
                    agent_code=AGENT_CODE,
                    profile_code=PROFILE_CODE
                )

                assert result.migration_id == "TEST_123"
                assert result.migration_status == "PENDING"

# Run tests with pytest
# pytest test_voltarium.py -v
```

### Integration Testing with Real Staging Data

Voltarium provides real staging credentials for comprehensive testing:

```python
import asyncio
from voltarium.sandbox import RETAILERS, UTILITIES
from voltarium import VoltariumClient, CreateMigrationRequest

async def test_with_real_staging_data():
    """Test with real CCEE staging environment data."""

    # Use real staging credentials
    retailer = RETAILERS[0]

    async with VoltariumClient(
        base_url="https://staging.ccee.org.br",
        client_id=retailer.client_id,
        client_secret=retailer.client_secret
    ) as client:
        print(f"Testing with retailer {retailer.agent_code}")

        # Test listing migrations with real data
        migrations = client.list_migrations(
            initial_reference_month="2024-01",
            final_reference_month="2024-12",
            agent_code=str(retailer.agent_code),
            profile_code=str(retailer.profiles[0])
        )

        migration_count = 0
        async for migration in migrations:
            migration_count += 1
            print(f"Found migration: {migration.migration_id}")

            # Test getting individual migration
            detailed = await client.get_migration(
                migration_id=migration.migration_id,
                agent_code=str(retailer.agent_code),
                profile_code=str(retailer.profiles[0])
            )

            assert detailed.migration_id == migration.migration_id
            break  # Test just first one

        print(f"Total migrations found: {migration_count}")
        return migration_count

def explore_available_staging_data():
    """Explore available staging credentials."""

    print("Available Retailers:")
    for i, retailer in enumerate(RETAILERS[:5]):  # Show first 5
        print(f"  {i}: Agent {retailer.agent_code}, Profiles: {retailer.profiles}")

    print("\nAvailable Utilities:")
    for i, utility in enumerate(UTILITIES[:5]):  # Show first 5
        print(f"  {i}: Agent {utility.agent_code}, Profiles: {utility.profiles}")

    print(f"\nTotal: {len(RETAILERS)} retailers, {len(UTILITIES)} utilities")

async def test_cross_agent_scenarios():
    """Test scenarios involving different agents."""

    retailer = RETAILERS[0]
    utility = UTILITIES[0]

    print(f"Testing migration between retailer {retailer.agent_code} and utility {utility.agent_code}")

    # Test with retailer credentials
    async with VoltariumClient(
        base_url="https://staging.ccee.org.br",
        client_id=retailer.client_id,
        client_secret=retailer.client_secret
    ) as client:

        # Create a test migration
        request = CreateMigrationRequest(
            consumer_unit_code="TEST_UC_001",
            utility_agent_code=utility.agent_code,
            document_type="CNPJ",
            document_number="12345678901234",
            retailer_agent_code=retailer.agent_code,
            reference_month="2024-06",
            denunciation_date="2024-06-15",
            retailer_profile_code=retailer.profiles[0],
            consumer_unit_email="test@staging.example.com",
            comment="Staging test migration"
        )

        try:
            migration = await client.create_migration(
                migration_data=request,
                agent_code=str(retailer.agent_code),
                profile_code=str(retailer.profiles[0])
            )
            print(f"✅ Created test migration: {migration.migration_id}")

            # Test updating the migration
            from voltarium import UpdateMigrationRequest
            update_request = UpdateMigrationRequest(
                reference_month="2024-07",
                retailer_profile_code=retailer.profiles[0],
                document_type="CNPJ",
                document_number="12345678901234",
                consumer_unit_email="updated@staging.example.com"
            )

            updated_migration = await client.update_migration(
                migration_id=migration.migration_id,
                migration_data=update_request,
                agent_code=str(retailer.agent_code),
                profile_code=str(retailer.profiles[0])
            )
            print(f"✅ Updated migration: {updated_migration.migration_id}")

            # Clean up - delete the test migration
            await client.delete_migration(
                migration_id=migration.migration_id,
                agent_code=str(retailer.agent_code),
                profile_code=str(retailer.profiles[0])
            )
            print("✅ Cleaned up test migration")

        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()

# Run staging tests
if __name__ == "__main__":
    print("🔍 Exploring staging data...")
    explore_available_staging_data()

    print("\n🧪 Testing with real staging data...")
    asyncio.run(test_with_real_staging_data())

    print("\n🔄 Testing cross-agent scenarios...")
    asyncio.run(test_cross_agent_scenarios())
```

### Available Staging Data

The staging environment includes:

- **30+ Retailers**: Agent codes 200000-200049
- **30+ Utilities**: Agent codes 100000-100009 and 400000-400019
- **Multiple Profiles**: Each agent has 1-2 profile codes for different scenarios
- **Real Credentials**: Working OAuth2 client IDs and secrets

Example usage:

```python
from voltarium.sandbox import RETAILERS, UTILITIES

# Pick any retailer for testing
retailer = RETAILERS[5]  # Agent 200005 with profiles [200150, 200151]

# Pick any utility for testing
utility = UTILITIES[2]  # Agent 100002 with profile [100002]

# Use in your tests
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

## Configuration Management

### Environment-Based Configuration

```python
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class VoltariumConfig:
    """Configuration class for Voltarium client."""
    base_url: str
    client_id: str
    client_secret: str
    timeout: float = 30.0
    max_retries: int = 3
    agent_code: Optional[str] = None
    profile_code: Optional[str] = None

    @classmethod
    def from_environment(cls) -> "VoltariumConfig":
        """Create configuration from environment variables."""
        return cls(
            base_url=os.getenv("CCEE_BASE_URL", "https://api.ccee.org.br"),
            client_id=os.getenv("CCEE_CLIENT_ID"),
            client_secret=os.getenv("CCEE_CLIENT_SECRET"),
            timeout=float(os.getenv("CCEE_TIMEOUT", "30.0")),
            max_retries=int(os.getenv("CCEE_MAX_RETRIES", "3")),
            agent_code=os.getenv("CCEE_AGENT_CODE"),
            profile_code=os.getenv("CCEE_PROFILE_CODE")
        )

    def validate(self) -> None:
        """Validate configuration."""
        if not self.client_id:
            raise ValueError("CCEE_CLIENT_ID is required")
        if not self.client_secret:
            raise ValueError("CCEE_CLIENT_SECRET is required")
        if not self.base_url:
            raise ValueError("CCEE_BASE_URL is required")

async def configured_client_example():
    """Example using configuration management."""
    config = VoltariumConfig.from_environment()
    config.validate()

    client_params = {
        "base_url": config.base_url,
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "timeout": config.timeout,
        "max_retries": config.max_retries
    }

    async with VoltariumClient(**client_params) as client:
        # Use the configured client
        migrations = client.list_migrations(
            initial_reference_month="2024-01",
            final_reference_month="2024-12",
            agent_code=config.agent_code or AGENT_CODE,
            profile_code=config.profile_code or PROFILE_CODE
        )

        async for migration in migrations:
            print(f"Migration: {migration.migration_id}")
            break  # Just show first one

# Run the example
if __name__ == "__main__":
    asyncio.run(configured_client_example())
```
