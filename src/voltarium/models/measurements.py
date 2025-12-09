"""Measurement models for CCEE API (varejista/consumo/medicoes)."""

from pydantic import BaseModel, ConfigDict, Field


class Measurement(BaseModel):
    """Consumption measurement model (Portuguese: medicao).

    This model represents consumption measurements sent by utilities to retailers.
    Uses permissive configuration to accommodate schema variations across environments.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    measurement_consumption_id: str = Field(
        alias="identificadorMedicaoConsumo", description="Measurement consumption identifier"
    )
    consumer_unit_code: str = Field(alias="codigoUnidadeConsumidora", description="Consumer unit code")
    utility_agent_code: int = Field(alias="codigoAgenteConcessionaria", description="Utility agent code")
    reference_day: str = Field(alias="diaReferencia", description="Reference day")
    consumption_reference_date: str = Field(alias="dataReferenciaConsumo", description="Consumption reference date")
    consumption: float = Field(alias="consumo", description="Consumption value")
    consumption_type: str = Field(alias="tipoConsumo", description="Consumption type (e.g., AJUSTADO)")
    update_date: str = Field(alias="dataAtualizacao", description="Last update date")
    measurement_status: str = Field(
        alias="situacaoMedicao", description="Measurement status (CONSISTIDA, REJEITADA, etc.)"
    )
