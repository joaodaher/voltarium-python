import asyncio
from datetime import timedelta

from tests.base import SandboxTestCase
from voltarium.factories import CreateMigrationRequestFactory, UpdateMigrationRequestFactory
from voltarium.models import MigrationItem, MigrationListItem


class TestMigrationClient(SandboxTestCase):
    """Integration tests for migration endpoints."""

    async def test_migration_full_lifecycle_integration(self) -> None:
        """
        Comprehensive integration test covering the full migration lifecycle:
        1. Create migration
        2. Update migration
        3. Fetch migration
        4. Create bulk migrations
        5. List migrations
        """
        # Store created migration IDs for cleanup and testing
        migrations: list[MigrationItem] = []

        # 1. Create Migration Test
        # Use factory with specific test setup credentials
        create_request = CreateMigrationRequestFactory.build(
            retailer_agent_code=self.agent_id,
            retailer_profile_code=self.profile_id,
            utility_agent_code=self.utility_id,
        )

        result = await self.client.create_migration(
            migration_data=create_request,
            agent_code=self.agent_id,
            profile_code=self.profile_id,
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, MigrationItem)
        migrations.append(result)

        print(f"✓ Created migration: {result}")
        print(f"  - Agent: {create_request.retailer_agent_code}")
        print(f"  - Profile: {create_request.retailer_profile_code}")
        print(f"  - Month: {create_request.reference_month}")

        # 2. Update Migration Test
        if not migrations:
            self.fail("No migrations created to update.")

        migration_id = migrations[0].migration_id

        future_date = migrations[0].reference_date + timedelta(days=60)
        update_request = UpdateMigrationRequestFactory.build(
            retailer_profile_code=self.profile_id,
            reference_month=future_date.strftime("%Y-%m"),
        )
        result = await self.client.update_migration(
            migration_id=migration_id,
            migration_data=update_request,
            agent_code=self.agent_id,
            profile_code=self.profile_id,
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, MigrationItem)

        print(f"✓ Updated migration: {migration_id}")

        # 3. Fetch Migration Test
        if not migrations:
            self.fail("No migrations created to fetch.")

        migration_id = migrations[0].migration_id

        result = await self.client.get_migration(
            migration_id=migration_id,
            agent_code=self.agent_id,
            profile_code=self.profile_id,
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, MigrationItem)

        print(f"✓ Fetched migration: {result.migration_id}")
        print(f"  - Status: {result.migration_status}")

        # 4. Create Bulk Migrations Test
        k = 30  # Number of bulk migrations to create
        bulk_requests = [
            CreateMigrationRequestFactory.build(
                retailer_agent_code=self.agent_id,
                retailer_profile_code=self.profile_id,
                utility_agent_code=self.utility_id,
            )
            for _ in range(k)
        ]

        tasks = [
            self.client.create_migration(
                migration_data=create_request,
                agent_code=self.agent_id,
                profile_code=self.profile_id,
            )
            for create_request in bulk_requests
        ]

        results = await asyncio.gather(*tasks)

        for i, result in enumerate(results):
            self.assertIsNotNone(result)
            migrations.append(result)
            print(f"✓ Created bulk migration {i + 1}: {result}")

        # 5. List Migrations Test

        earliest_month = min([m.reference_date for m in migrations])
        latest_month = max([m.reference_date for m in migrations])

        result = self.client.list_migrations(
            initial_reference_month=earliest_month.strftime("%Y-%m"),
            final_reference_month=latest_month.strftime("%Y-%m"),
            agent_code=self.agent_id,
            profile_code=self.profile_id,
        )
        retrieved_migrations = [migration async for migration in result]

        # Should have at least the migrations we created
        self.assertGreaterEqual(len(retrieved_migrations), k)

        for migration in retrieved_migrations:
            self.assertIsInstance(migration, MigrationListItem)

        print(f"✓ Listed {len(retrieved_migrations)} migrations")

        print("\n✓ Integration test completed successfully!")
        print(f"   Total migrations created: {len(migrations)}")
        print(f"   Using agent: {self.agent_id} (profile: {self.profile_id})")
        print(f"   Using concessionaria: {self.utility_id}")
