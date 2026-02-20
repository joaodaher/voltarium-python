"""Unit tests for Measurement model parsing from CCEE API responses."""

import json
from pathlib import Path

from voltarium.models.measurements import Measurement


def _fixture_path(name: str) -> Path:
    return Path(__file__).parent.parent / "fixtures" / "measurements" / name


class TestMeasurementFromRawApiResponse:
    """Test Measurement.model_validate with real CCEE API payload structures."""

    def test_parses_consistida_measurement_with_int_utility_code(self) -> None:
        """Parse measurement with integer codigoAgenteConcessionaria (common in API)."""
        raw = {
            "identificadorMedicaoConsumo": "UC-TESTE-202409-001",
            "codigoUnidadeConsumidora": "UC-TESTE",
            "codigoAgenteConcessionaria": 100004,
            "diaReferencia": "2024-09-15",
            "dataReferenciaConsumo": "2024-09-15T00:00:00-03:00",
            "consumo": 15432.5,
            "tipoConsumo": "AJUSTADO",
            "dataAtualizacao": "2024-09-20T14:32:10-03:00",
            "situacaoMedicao": "CONSISTIDA",
        }
        m = Measurement.model_validate(raw)
        assert m.measurement_consumption_id == "UC-TESTE-202409-001"
        assert m.consumer_unit_code == "UC-TESTE"
        assert m.utility_agent_code == 100004
        assert m.reference_day == "2024-09-15"
        assert m.consumption_reference_date == "2024-09-15T00:00:00-03:00"
        assert m.consumption == 15432.5
        assert m.consumption_type == "AJUSTADO"
        assert m.update_date == "2024-09-20T14:32:10-03:00"
        assert m.measurement_status == "CONSISTIDA"

    def test_parses_measurement_with_string_utility_code(self) -> None:
        """Parse measurement with string codigoAgenteConcessionaria (API may return either)."""
        raw = {
            "identificadorMedicaoConsumo": "UC123456-202410-001",
            "codigoUnidadeConsumidora": "UC123456",
            "codigoAgenteConcessionaria": "100005",
            "diaReferencia": "2024-10-01",
            "dataReferenciaConsumo": "2024-10-01T00:00:00-03:00",
            "consumo": 0.0,
            "tipoConsumo": "ESTIMADO",
            "dataAtualizacao": "2024-10-05T11:00:00-03:00",
            "situacaoMedicao": "REJEITADA",
        }
        m = Measurement.model_validate(raw)
        assert m.utility_agent_code == 100005
        assert m.consumption == 0.0
        assert m.measurement_status == "REJEITADA"
        assert m.consumption_type == "ESTIMADO"

    def test_parses_all_consumption_types(self) -> None:
        """Verify AJUSTADO, MEDIDO, ESTIMADO are parsed correctly."""
        for tipo in ("AJUSTADO", "MEDIDO", "ESTIMADO"):
            raw = {
                "identificadorMedicaoConsumo": f"id-{tipo}",
                "codigoUnidadeConsumidora": "UC001",
                "codigoAgenteConcessionaria": 100000,
                "diaReferencia": "2024-09-01",
                "dataReferenciaConsumo": "2024-09-01T00:00:00-03:00",
                "consumo": 100.0,
                "tipoConsumo": tipo,
                "dataAtualizacao": "2024-09-02T00:00:00-03:00",
                "situacaoMedicao": "CONSISTIDA",
            }
            m = Measurement.model_validate(raw)
            assert m.consumption_type == tipo

    def test_parses_all_measurement_statuses(self) -> None:
        """Verify CONSISTIDA and REJEITADA are parsed correctly."""
        for status in ("CONSISTIDA", "REJEITADA"):
            raw = {
                "identificadorMedicaoConsumo": f"id-{status}",
                "codigoUnidadeConsumidora": "UC001",
                "codigoAgenteConcessionaria": 100000,
                "diaReferencia": "2024-09-01",
                "dataReferenciaConsumo": "2024-09-01T00:00:00-03:00",
                "consumo": 50.0,
                "tipoConsumo": "MEDIDO",
                "dataAtualizacao": "2024-09-02T00:00:00-03:00",
                "situacaoMedicao": status,
            }
            m = Measurement.model_validate(raw)
            assert m.measurement_status == status

    def test_extra_fields_allowed(self) -> None:
        """Model has extra='allow' to accommodate API schema variations."""
        raw = {
            "identificadorMedicaoConsumo": "id-extra",
            "codigoUnidadeConsumidora": "UC001",
            "codigoAgenteConcessionaria": 100000,
            "diaReferencia": "2024-09-01",
            "dataReferenciaConsumo": "2024-09-01T00:00:00-03:00",
            "consumo": 100.0,
            "tipoConsumo": "AJUSTADO",
            "dataAtualizacao": "2024-09-02T00:00:00-03:00",
            "situacaoMedicao": "CONSISTIDA",
            "campoExtraNaoDocumentado": "valor",
        }
        m = Measurement.model_validate(raw)
        assert m.measurement_consumption_id == "id-extra"


class TestMeasurementFromFixtureFiles:
    """Test parsing from fixture files (real API response structure)."""

    def test_parses_raw_api_response_fixture(self) -> None:
        """Parse full API response with medicoes array."""
        path = _fixture_path("raw_api_response.json")
        data = json.loads(path.read_text())
        medicoes = data["medicoes"]
        assert len(medicoes) == 3

        parsed = [Measurement.model_validate(m) for m in medicoes]
        assert parsed[0].measurement_consumption_id == "UC-TESTE-202409-001"
        assert parsed[0].consumption == 15432.5
        assert parsed[0].measurement_status == "CONSISTIDA"

        assert parsed[1].measurement_consumption_id == "UC-TESTE-202409-002"
        assert parsed[1].consumption == 892.75
        assert parsed[1].consumption_type == "MEDIDO"

        assert parsed[2].measurement_consumption_id == "UC123456-202410-001"
        assert parsed[2].utility_agent_code == 100005
        assert parsed[2].measurement_status == "REJEITADA"

    def test_parses_paginated_response_fixture(self) -> None:
        """Parse paginated response with indexProximaPagina."""
        path = _fixture_path("paginated_response_page1.json")
        data = json.loads(path.read_text())
        medicoes = data["medicoes"]
        assert len(medicoes) == 1
        assert data["indexProximaPagina"] == "eyJwYWdlIjoiMiJ9"

        m = Measurement.model_validate(medicoes[0])
        assert m.measurement_consumption_id == "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        assert m.consumer_unit_code == "UC789012"
        assert m.utility_agent_code == 400004
        assert m.consumption == 12500.0

    def test_parses_empty_response_fixture(self) -> None:
        """Parse empty medicoes array."""
        path = _fixture_path("empty_response.json")
        data = json.loads(path.read_text())
        assert data["medicoes"] == []
        assert data["indexProximaPagina"] is None

        parsed = [Measurement.model_validate(m) for m in data["medicoes"]]
        assert parsed == []


class TestMeasurementSerialization:
    """Test Measurement serialization to API format."""

    def test_model_dump_by_alias_produces_portuguese_keys(self) -> None:
        """Serialization with by_alias produces CCEE API field names."""
        m = Measurement.model_validate(
            {
                "identificadorMedicaoConsumo": "id-1",
                "codigoUnidadeConsumidora": "UC001",
                "codigoAgenteConcessionaria": 100004,
                "diaReferencia": "2024-09-15",
                "dataReferenciaConsumo": "2024-09-15T00:00:00-03:00",
                "consumo": 1000.0,
                "tipoConsumo": "AJUSTADO",
                "dataAtualizacao": "2024-09-20T00:00:00-03:00",
                "situacaoMedicao": "CONSISTIDA",
            }
        )
        dumped = m.model_dump(by_alias=True)
        assert dumped["identificadorMedicaoConsumo"] == "id-1"
        assert dumped["codigoUnidadeConsumidora"] == "UC001"
        assert dumped["codigoAgenteConcessionaria"] == 100004
        assert dumped["diaReferencia"] == "2024-09-15"
        assert dumped["consumo"] == 1000.0
        assert dumped["situacaoMedicao"] == "CONSISTIDA"


class TestMeasurementFactory:
    """Test MeasurementFactory produces valid API-compatible instances."""

    def test_factory_build_produces_valid_measurement(self) -> None:
        """MeasurementFactory.build() produces valid Measurement."""
        from voltarium.factories.measurements import MeasurementFactory

        m = MeasurementFactory.build()
        assert m.measurement_consumption_id
        assert m.consumer_unit_code
        assert m.utility_agent_code
        assert m.reference_day
        assert m.consumption_reference_date.endswith("-03:00")
        assert m.consumption >= 0
        assert m.consumption_type in ("AJUSTADO", "MEDIDO", "ESTIMADO")
        assert m.measurement_status in ("CONSISTIDA", "REJEITADA")

    def test_factory_build_measurement_id_format(self) -> None:
        """Measurement ID follows UC-CODE-YYYYMM-NNN pattern when using sandbox codes."""
        from voltarium.factories.measurements import MeasurementFactory

        m = MeasurementFactory.build(consumer_unit_code="UC-TESTE", reference_day="2024-09-15")
        assert m.measurement_consumption_id.startswith("UC-TESTE-202409-")
        assert m.consumption_reference_date == "2024-09-15T00:00:00-03:00"

    def test_factory_serializes_to_api_format(self) -> None:
        """Factory-built Measurement serializes to valid CCEE API format."""
        from voltarium.factories.measurements import MeasurementFactory

        m = MeasurementFactory.build()
        dumped = m.model_dump(by_alias=True)
        assert "identificadorMedicaoConsumo" in dumped
        assert "codigoUnidadeConsumidora" in dumped
        assert "codigoAgenteConcessionaria" in dumped
        assert "diaReferencia" in dumped
        assert "consumo" in dumped
        assert "situacaoMedicao" in dumped
