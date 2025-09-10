"""Contract models for CCEE API (varejista/contratos)."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Contract(BaseModel):
    """Retailer contract model.

    This model is intentionally permissive to accommodate schema variations
    across environments. Known fields are declared with Portuguese aliases
    to match the CCEE API, and additional fields are accepted.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    contract_id: str = Field(alias="idContrato", description="Contract ID")
    consumer_unit_code: str | None = Field(
        default=None, alias="codigoUnidadeConsumidora", description="Consumer unit code"
    )
    retailer_agent_code: int | None = Field(
        default=None, alias="codigoAgenteVarejista", description="Retailer agent code"
    )
    utility_agent_code: int | None = Field(
        default=None, alias="codigoAgenteConcessionaria", description="Utility agent code"
    )
    document_type: str | None = Field(default=None, alias="tipoDocumento", description="Document type")
    document_number: str | None = Field(default=None, alias="numeroDocumento", description="Document number")
    start_date: datetime | None = Field(default=None, alias="dataInicio", description="Start date")
    end_date: datetime | None = Field(default=None, alias="dataFim", description="End date")
    reference_month: datetime | None = Field(default=None, alias="mesReferencia", description="Reference month")
    contract_status: str | None = Field(default=None, alias="statusContrato", description="Contract status")


class CreateContractRequest(BaseModel):
    """Request body for creating a retailer contract.

    Uses Portuguese field aliases to match the CCEE API and allows
    extra fields for forward compatibility across environments.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    utility_agent_code: int | str = Field(
        serialization_alias="codigoAgenteConcessionaria", description="Utility agent code"
    )
    consumer_unit_code: str = Field(serialization_alias="codigoUnidadeConsumidora", description="Consumer unit code")
    consumer_unit_address: str | None = Field(
        default=None,
        serialization_alias="enderecoUnidadeConsumidora",
        description="Consumer unit address (free text)",
    )
    consumer_unit_name: str | None = Field(
        default=None, serialization_alias="nomeUnidadeConsumidora", description="Consumer unit name"
    )

    # Legal representatives (minimal schema, extra allowed)
    representantes_legais: list[dict] | None = Field(
        default=None,
        serialization_alias="representantesLegais",
        description="List of legal representatives",
    )
    document_type: Literal["CNPJ", "CPF"] = Field(serialization_alias="tipoDocumento", description="Document type")
    document_number: str = Field(serialization_alias="numeroDocumento", description="Document number")
    # Additional optional fields per docs
    consumer_unit_phone: str | None = Field(
        default=None, serialization_alias="telefoneUnidadeConsumidora", description="Consumer unit phone"
    )
    branch_consumer_unit_cnpj: str | None = Field(
        default=None,
        serialization_alias="cnpjFilialUnidadeConsumidora",
        description="Branch CNPJ for consumer unit",
    )
    branch_consumer_unit_address: str | None = Field(
        default=None,
        serialization_alias="enderecoFilialUnidadeConsumidora",
        description="Branch address for consumer unit",
    )

    @field_validator("document_number")
    def validate_document_number(cls, v: str) -> str:
        v = "".join(filter(str.isdigit, v))
        if not v.isdigit():
            raise ValueError("document_number must be a number")
        return v
