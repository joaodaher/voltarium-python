"""Integration tests for measurements endpoints."""

import pytest

from voltarium.client import VoltariumClient
from voltarium.exceptions import ValidationError
from voltarium.models.measurements import Measurement
from voltarium.sandbox import SandboxAgentCredentials


async def test_measurements_list_integration(
    client: VoltariumClient,
    retailer: SandboxAgentCredentials,
    utility: SandboxAgentCredentials,
) -> None:
    """Test listing measurements with required parameters and filters."""
    profile_id = retailer.profiles[0]

    # 01. LIST measurements with required parameters
    measurements_iter = client.list_measurements(
        consumer_unit_code="UC-TESTE",
        utility_agent_code=utility.agent_code,
        start_datetime="2024-09-01T00:00:00-03:00",
        end_datetime="2024-09-30T23:59:59-03:00",
        agent_code=retailer.agent_code,
        profile_code=profile_id,
    )
    measurements = [m async for m in measurements_iter]

    # The list might be empty in sandbox, but the call should succeed
    assert isinstance(measurements, list)

    # If we got results, verify they're valid Measurement objects with full schema
    for measurement in measurements:
        assert isinstance(measurement, Measurement)
        assert measurement.measurement_consumption_id
        assert measurement.consumer_unit_code
        assert measurement.utility_agent_code
        assert measurement.reference_day
        assert measurement.consumption_reference_date
        assert isinstance(measurement.consumption, (int, float))
        assert measurement.consumption_type in ("AJUSTADO", "MEDIDO", "ESTIMADO")
        assert measurement.update_date
        assert measurement.measurement_status in ("CONSISTIDA", "REJEITADA")

    # 02. LIST measurements with status filter
    filtered_iter = client.list_measurements(
        consumer_unit_code="UC-TESTE",
        utility_agent_code=utility.agent_code,
        start_datetime="2024-09-01T00:00:00-03:00",
        end_datetime="2024-09-30T23:59:59-03:00",
        agent_code=retailer.agent_code,
        profile_code=profile_id,
        measurement_status="CONSISTIDA",
    )
    filtered_measurements = [m async for m in filtered_iter]

    # Verify all returned measurements have the correct status (if any)
    for measurement in filtered_measurements:
        assert measurement.measurement_status == "CONSISTIDA"


async def test_measurements_list_with_string_utility_code(
    client: VoltariumClient,
    retailer: SandboxAgentCredentials,
    utility: SandboxAgentCredentials,
) -> None:
    """Test listing measurements with utility_agent_code as string (API accepts both)."""
    profile_id = retailer.profiles[0]

    measurements_iter = client.list_measurements(
        consumer_unit_code="UC-TESTE",
        utility_agent_code=str(utility.agent_code),
        start_datetime="2024-09-01T00:00:00-03:00",
        end_datetime="2024-09-30T23:59:59-03:00",
        agent_code=retailer.agent_code,
        profile_code=profile_id,
    )
    measurements = [m async for m in measurements_iter]
    assert isinstance(measurements, list)
    for m in measurements:
        assert isinstance(m.utility_agent_code, int)


async def test_measurements_list_rejeitada_filter(
    client: VoltariumClient,
    retailer: SandboxAgentCredentials,
    utility: SandboxAgentCredentials,
) -> None:
    """Test listing measurements filtered by REJEITADA status."""
    profile_id = retailer.profiles[0]

    measurements_iter = client.list_measurements(
        consumer_unit_code="UC-TESTE",
        utility_agent_code=utility.agent_code,
        start_datetime="2024-09-01T00:00:00-03:00",
        end_datetime="2024-09-30T23:59:59-03:00",
        agent_code=retailer.agent_code,
        profile_code=profile_id,
        measurement_status="REJEITADA",
    )
    measurements = [m async for m in measurements_iter]
    for m in measurements:
        assert m.measurement_status == "REJEITADA"


async def test_measurements_dates_different_months_success(
    client: VoltariumClient,
    retailer: SandboxAgentCredentials,
    utility: SandboxAgentCredentials,
) -> None:
    """Test that dates spanning multiple months are handled transparently (split by month)."""
    profile_id = retailer.profiles[0]

    measurements_iter = client.list_measurements(
        consumer_unit_code="UC-TESTE",
        utility_agent_code=utility.agent_code,
        start_datetime="2024-09-01T00:00:00-03:00",
        end_datetime="2024-10-31T23:59:59-03:00",  # Spans Sep and Oct
        agent_code=retailer.agent_code,
        profile_code=profile_id,
    )
    measurements = [m async for m in measurements_iter]

    # Should succeed (no ERR_PERIODO_INVALIDO_MEDICOES); list may be empty in sandbox
    assert isinstance(measurements, list)


async def test_measurements_dates_before_implementation_error(
    client: VoltariumClient,
    retailer: SandboxAgentCredentials,
    utility: SandboxAgentCredentials,
) -> None:
    """Test that dates before 08/2024 raise ERR_SISTEMA_MIGRACAO_IMPLATADO_MEDICOES."""
    profile_id = retailer.profiles[0]

    with pytest.raises(ValidationError) as exc_info:
        measurements_iter = client.list_measurements(
            consumer_unit_code="UC-TESTE",
            utility_agent_code=utility.agent_code,
            start_datetime="2024-03-01T00:00:00-03:00",  # Before 08/2024
            end_datetime="2024-03-31T23:59:59-03:00",
            agent_code=retailer.agent_code,
            profile_code=profile_id,
        )
        _ = [m async for m in measurements_iter]

    assert "ERR_SISTEMA_MIGRACAO_IMPLATADO_MEDICOES" in exc_info.value.code
