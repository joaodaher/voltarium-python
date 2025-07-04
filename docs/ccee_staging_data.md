# CCEE Staging Data Usage Guide

This document explains how to use the predefined CCEE staging environment data for testing your Voltarium applications.

## Overview

The CCEE staging environment provides predefined agent codes, credentials, and perfil data that you must use for testing. The `voltarium.data` module contains all this structured data to ensure your tests use valid staging credentials.

## Available Data

### Varejistas (Retailers)
- **30 total varejistas** with codes: 200000-200009 and 200030-200049
- Each varejista has:
  - `client_id` and `client_secret` for OAuth authentication
  - `agent_code` for API operations
  - Two perfil codes (`perfil_1` and `perfil_2`)

### Concessionarias (Utilities)
- **30 total concessionarias** with codes: 100000-100009 and 400000-400019
- Each concessionaria has:
  - `client_id` and `client_secret` for OAuth authentication
  - `agent_code` for API operations
  - No perfil codes (concessionarias don't use perfils)

### Submercados (Markets)
- Four Brazilian energy submercados: `"SE"`, `"S"`, `"NE"`, `"N"`

## Basic Usage

### Import the data module
```python
from voltarium.data import (
    get_random_varejista,
    get_random_concessionaria,
    get_varejista_by_code,
    VAREJISTAS,
    CONCESSIONARIAS,
)
```

### Get random credentials for testing
```python
# Get a random varejista for testing
varejista = get_random_varejista()
print(f"Client ID: {varejista.client_id}")
print(f"Agent Code: {varejista.agent_code}")
print(f"Perfil 1: {varejista.perfil_1}")

# Get a random concessionaria
concessionaria = get_random_concessionaria()
print(f"Client ID: {concessionaria.client_id}")
print(f"Agent Code: {concessionaria.agent_code}")
```

### Get specific credentials by code
```python
# Get specific varejista by agent code
varejista = get_varejista_by_code(200000)
if varejista:
    print(f"Found: {varejista.client_id}")

# Get specific concessionaria by agent code
concessionaria = get_concessionaria_by_code(100000)
if concessionaria:
    print(f"Found: {concessionaria.client_id}")
```

## Testing with Fixtures

### Using the provided fixtures
```python
def test_api_call(agent_credentials):
    """Test using the agent_credentials fixture."""
    client = VoltariumClient(
        base_url="https://staging.ccee.org.br",
        client_id=agent_credentials["client_id"],
        client_secret=agent_credentials["client_secret"]
    )
    # Your test code here...

def test_with_full_varejista_data(staging_varejista_credentials):
    """Test using the full varejista data fixture."""
    creds = staging_varejista_credentials
    print(f"Testing with agent {creds.agent_code}")
    print(f"Using perfil {creds.perfil_1}")
    # Your test code here...
```

## Factory Usage

The factories now automatically use realistic staging data:

```python
from voltarium.factories import MigrationListItemFactory

# Create a migration with realistic staging data
migration = MigrationListItemFactory()

# Will use real agent codes from CCEE staging
print(f"Varejista: {migration.codigoAgenteVarejista}")  # e.g., 200035
print(f"Concessionaria: {migration.codigoAgenteConcessionaria}")  # e.g., 100005
print(f"Perfil: {migration.codigoPerfilVarejista}")  # e.g., 200350
print(f"Submercado: {migration.submercado}")  # e.g., "SE"
```

## Real API Testing

When testing against the real CCEE staging environment:

```python
@pytest.mark.integration
async def test_real_api_migration_list(staging_varejista_credentials):
    """Test against real CCEE staging API."""
    async with VoltariumClient(
        base_url="https://staging.ccee.org.br/api",
        client_id=staging_varejista_credentials.client_id,
        client_secret=staging_varejista_credentials.client_secret,
    ) as client:
        # This will use real staging credentials
        migrations = await client.list_migrations()
        assert isinstance(migrations, list)
```

## Key Benefits

1. **✅ No Authentication Errors**: Uses real staging credentials
2. **✅ Valid Agent Codes**: All codes exist in staging environment
3. **✅ Correct Perfil Mapping**: Perfils match their respective agents
4. **✅ Realistic Data**: Your tests use data that mirrors production
5. **✅ Easy Expansion**: Ready to support concessionarias when needed

## Migration from Fake Data

If you were using fake factory data before:

### Before (Fake Data)
```python
# Old factory with fake data
migration = MigrationListItemFactory()
# Might generate: codigoAgenteVarejista=9999 (invalid!)
```

### After (Staging Data)
```python
# New factory with real staging data
migration = MigrationListItemFactory()
# Will generate: codigoAgenteVarejista=200035 (valid staging code!)
```

The change is automatic - your existing factory usage continues to work but now uses realistic data.

## Important Notes

- **Varejista Focus**: Currently optimized for varejista testing (as per requirements)
- **Concessionaria Ready**: Full concessionaria data available for future expansion
- **Staging Only**: This data is specifically for the CCEE staging environment
- **No Production Data**: Never use this data against production systems
