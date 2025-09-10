from voltarium.client import VoltariumClient
from voltarium.factories import CreateContractRequestFactory
from voltarium.models import Contract
from voltarium.sandbox import SandboxAgentCredentials


async def test_contracts_full_lifecycle_integration(
    client: VoltariumClient,
    retailer: SandboxAgentCredentials,
    utility: SandboxAgentCredentials,
) -> None:
    profile_id = retailer.profiles[0]

    # 01. CREATE contract
    created: Contract | None = None

    create_req = CreateContractRequestFactory.build(
        retailer_agent_code=retailer.agent_code,
        retailer_profile_code=profile_id,
        utility_agent_code=utility.agent_code,
    )
    created = await client.create_contract(
        contract_data=create_req,
        agent_code=retailer.agent_code,
        profile_code=profile_id,
    )
    assert isinstance(created, Contract)
    assert created.contract_id

    # 02. GET contract by id
    fetched = await client.get_contract(
        contract_id=created.contract_id,
        agent_code=retailer.agent_code,
        profile_code=profile_id,
    )
    assert isinstance(fetched, Contract)
    assert fetched.contract_id == created.contract_id

    # 03. LIST contracts with utility filter
    contracts_iter = client.list_contracts(
        initial_reference_month="2020-01",
        final_reference_month="2030-12",
        agent_code=retailer.agent_code,
        profile_code=profile_id,
        utility_agent_code=utility.agent_code,
    )
    retrieved = [c async for c in contracts_iter]
    assert isinstance(retrieved, list)
    assert isinstance(retrieved[0], Contract)
