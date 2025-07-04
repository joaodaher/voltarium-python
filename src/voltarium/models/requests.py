"""Request models for API headers and query parameters."""

from pydantic import BaseModel, ConfigDict, Field


class ApiHeaders(BaseModel):
    """Headers required for Brazilian API requests."""

    model_config = ConfigDict(populate_by_name=True)

    agent_code: str = Field(serialization_alias="codigoAgente", description="Agent code")
    profile_code: str = Field(serialization_alias="codigoPerfil", description="Profile code")


class ListMigrationsParams(BaseModel):
    """Query parameters for listing migrations."""

    model_config = ConfigDict(populate_by_name=True)

    initial_reference_month: str = Field(
        serialization_alias="mesReferenciaInicial", description="Start reference month (YYYY-MM)"
    )
    final_reference_month: str = Field(
        serialization_alias="mesReferenciaFinal", description="End reference month (YYYY-MM)"
    )
    retailer_profile_code: str = Field(serialization_alias="codigoPerfilVarejista", description="Retailer profile code")
    consumer_unit_code: str | None = Field(
        default=None, serialization_alias="codigoUC", description="Consumer unit code filter"
    )
    migration_status: str | None = Field(
        default=None, serialization_alias="statusMigracao", description="Migration status filter"
    )
    next_page_index: str | None = Field(
        default=None, serialization_alias="indexProximaPagina", description="Next page index for pagination"
    )
