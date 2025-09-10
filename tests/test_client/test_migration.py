import asyncio
from datetime import timedelta

from voltarium.client import VoltariumClient
from voltarium.factories import CreateMigrationRequestFactory, UpdateMigrationRequestFactory
from voltarium.models import MigrationItem, MigrationListItem
from voltarium.sandbox import SandboxAgentCredentials


async def test_migration_full_lifecycle_integration(
    client: VoltariumClient,
    retailer: SandboxAgentCredentials,
    utility: SandboxAgentCredentials,
) -> None:
    """
    Comprehensive integration test covering the full migration lifecycle:
    1. Create migration
    2. Update migration
    3. Fetch migration
    4. Create bulk migrations
    5. List migrations
    """
    profile_id = retailer.profiles[0]
    # Store created migration IDs for cleanup and testing
    migrations: list[MigrationItem] = []

    # 1. Create Migration Test
    create_request = CreateMigrationRequestFactory.build(
        retailer_agent_code=retailer.agent_code,
        retailer_profile_code=profile_id,
        utility_agent_code=utility.agent_code,
    )

    result = await client.create_migration(
        migration_data=create_request,
        agent_code=retailer.agent_code,
        profile_code=profile_id,
    )
    assert result is not None
    assert isinstance(result, MigrationItem)
    migrations.append(result)

    # 2. Update Migration Test
    migration_id = migrations[0].migration_id
    future_date = migrations[0].reference_date + timedelta(days=60)
    update_request = UpdateMigrationRequestFactory.build(
        retailer_profile_code=profile_id,
        reference_month=future_date.strftime("%Y-%m"),
    )
    result = await client.update_migration(
        migration_id=migration_id,
        migration_data=update_request,
        agent_code=retailer.agent_code,
        profile_code=profile_id,
    )
    assert result is not None
    assert isinstance(result, MigrationItem)

    # 3. Fetch Migration Test
    result = await client.get_migration(
        migration_id=migration_id,
        agent_code=retailer.agent_code,
        profile_code=profile_id,
    )
    assert result is not None
    assert isinstance(result, MigrationItem)

    # 4. Create Bulk Migrations Test
    k = 30  # Number of bulk migrations to create
    bulk_requests = [
        CreateMigrationRequestFactory.build(
            retailer_agent_code=retailer.agent_code,
            retailer_profile_code=profile_id,
            utility_agent_code=utility.agent_code,
        )
        for _ in range(k)
    ]

    tasks = [
        client.create_migration(
            migration_data=create_request,
            agent_code=retailer.agent_code,
            profile_code=profile_id,
        )
        for create_request in bulk_requests
    ]

    results = await asyncio.gather(*tasks)

    for result in results:
        assert result is not None
        migrations.append(result)

    # 5. List Migrations Test
    earliest_month = min([m.reference_date for m in migrations])
    latest_month = max([m.reference_date for m in migrations])

    result_iter = client.list_migrations(
        initial_reference_month=earliest_month.strftime("%Y-%m"),
        final_reference_month=latest_month.strftime("%Y-%m"),
        agent_code=retailer.agent_code,
        profile_code=profile_id,
    )
    retrieved_migrations = [migration async for migration in result_iter]

    # Should have at least the migrations we created
    assert len(retrieved_migrations) >= k

    for migration in retrieved_migrations:
        assert isinstance(migration, MigrationListItem)
