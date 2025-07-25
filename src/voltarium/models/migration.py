"""Migration models for CCEE API."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from voltarium.models.constants import MigrationStatus


class BaseMigration(BaseModel):
    """Base migration model with common fields."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    migration_id: str = Field(alias="idMigracao", description="Migration ID")
    consumer_unit_code: str = Field(alias="codigoUnidadeConsumidora", description="Consumer unit code")
    utility_agent_consumer_unit_code: str = Field(
        alias="codigoAgenteConcessionariaUnidadeConsumidora", description="Utility agent consumer unit code"
    )
    utility_agent_code: int = Field(alias="codigoAgenteConcessionaria", description="Utility agent code")
    document_type: str = Field(alias="tipoDocumento", description="Document type")
    document_number: str = Field(alias="numeroDocumento", description="Document number")
    retailer_agent_code: int = Field(alias="codigoAgenteVarejista", description="Retailer agent code")
    request_date: datetime = Field(alias="dataSolicitacao", description="Request date")
    retailer_profile_code: int = Field(alias="codigoPerfilVarejista", description="Retailer profile code")
    migration_status: MigrationStatus = Field(alias="statusMigracao", description="Migration status")
    submarket: str | None = Field(default=None, alias="submercado", description="Submarket")
    dhc_value: float | None = Field(default=None, alias="valorDHC", description="DHC value")
    musd_value: float | None = Field(default=None, alias="valorMusd", description="MUSD value")
    penalty_payment: str | None = Field(default=None, alias="pagamentoMulta", description="Penalty payment")
    justification: str | None = Field(default=None, alias="justificativa", description="Justification")
    validation_date: datetime | None = Field(default=None, alias="dataValidacao", description="Validation date")
    consumer_unit_email: str = Field(alias="emailUnidadeConsumidora", description="Consumer unit email")
    comment: str | None = Field(default=None, alias="comentario", description="Comment")


class MigrationListItem(BaseMigration):
    """Migration list item model for list operations."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    # Fields specific to list representation
    supplier_agent_code: int | None = Field(
        default=None, alias="codigoAgenteSupridora", description="Supplier agent code"
    )
    reference_month: datetime = Field(alias="mesReferencia", description="Reference month")
    denunciation_date: datetime = Field(alias="dataDenuncia", description="Denunciation date")
    cer_celebration_id: str | None = Field(default=None, alias="idCelebracaoCER", description="CER celebration ID")


class MigrationItem(BaseMigration):
    """Migration item model for detailed operations (CRUD)."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    # Fields specific to detailed representation
    reference_date: datetime = Field(alias="dataReferencia", description="Reference date")
    denunciation_date: datetime | None = Field(default=None, alias="dataDenuncia", description="Denunciation date")
    connected_type: str | None = Field(default=None, alias="tipoConectado", description="Connected type")
    supplier_code: int | None = Field(default=None, alias="codigoSupridora", description="Supplier code")


class CreateMigrationRequest(BaseModel):
    """Request model for creating a migration."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    consumer_unit_code: str = Field(serialization_alias="codigoUnidadeConsumidora", description="Consumer unit code")
    utility_agent_code: int | str = Field(
        serialization_alias="codigoAgenteConcessionaria", description="Utility agent code"
    )
    document_type: Literal["CNPJ"] = Field(serialization_alias="tipoDocumento", description="Document type")
    document_number: str = Field(serialization_alias="numeroDocumento", description="Document number")
    retailer_agent_code: int | str = Field(
        serialization_alias="codigoAgenteVarejista", description="Retailer agent code"
    )
    reference_month: str = Field(serialization_alias="mesReferencia", description="Reference month")
    denunciation_date: str = Field(serialization_alias="dataDenuncia", description="Denunciation date")
    retailer_profile_code: int | str = Field(
        serialization_alias="codigoPerfilVarejista", description="Retailer profile code"
    )
    consumer_unit_email: str = Field(serialization_alias="emailUnidadeConsumidora", description="Consumer unit email")
    comment: str | None = Field(default=None, serialization_alias="comentario", description="Comment")

    @field_validator("document_number")
    def validate_document_number(cls, v: str) -> str:
        """Validate document number format."""
        # Remove all non-numeric characters
        v = "".join(filter(str.isdigit, v))
        # Check if the number is valid
        if not v.isdigit():
            raise ValueError("document_number must be a number")
        return v

    @field_validator("reference_month")
    def validate_reference_month(cls, v: str) -> str:
        """Validate reference month format."""
        # Validate the month format (YYYY-MM) and that it's a valid date
        try:
            datetime.strptime(v, "%Y-%m")
        except ValueError as exc:
            raise ValueError("reference_month must be in the format YYYY-MM") from exc
        return v

    @field_validator("denunciation_date")
    def validate_denunciation_date(cls, v: str) -> str:
        """Validate denunciation date format."""
        # Validate the date format (YYYY-MM-DD) and that it's a valid date
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("denunciation_date must be in the format YYYY-MM-DD") from exc
        return v


class UpdateMigrationRequest(BaseModel):
    """Request model for updating a migration."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    reference_month: str = Field(serialization_alias="mesReferencia", description="Reference month")
    retailer_profile_code: int = Field(serialization_alias="codigoPerfilVarejista", description="Retailer profile code")
    document_type: Literal["CNPJ"] = Field(serialization_alias="tipoDocumento", description="Document type")
    document_number: str = Field(serialization_alias="numeroDocumento", description="Document number")
    consumer_unit_email: str = Field(serialization_alias="emailUnidadeConsumidora", description="Consumer unit email")

    @field_validator("document_number")
    def validate_document_number(cls, v: str) -> str:
        """Validate document number format."""
        # Remove all non-numeric characters
        v = "".join(filter(str.isdigit, v))
        # Check if the number is valid
        if not v.isdigit():
            raise ValueError("document_number must be a number")
        return v

    @field_validator("reference_month")
    def validate_reference_month(cls, v: str) -> str:
        """Validate reference month format."""
        # Validate the month format (YYYY-MM) and that it's a valid date
        try:
            datetime.strptime(v, "%Y-%m")
        except ValueError as exc:
            raise ValueError("reference_month must be in the format YYYY-MM") from exc
        return v
