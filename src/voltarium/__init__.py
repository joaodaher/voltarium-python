"""Voltarium: Asynchronous Python client for CCEE API.

This package provides an asynchronous Python client for the CCEE
(Brazilian Electric Energy Commercialization Chamber) API.
"""

from voltarium.client import VoltariumClient
from voltarium.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
    VoltariumError,
)
from voltarium.models import (
    CreateMigrationRequest,
    MigrationItem,
    MigrationListItem,
    Token,
    UpdateMigrationRequest,
)
from voltarium.models.constants import MigrationStatus, Submarket

__all__ = [
    # Client
    "VoltariumClient",
    # Models
    "Token",
    "CreateMigrationRequest",
    "UpdateMigrationRequest",
    "MigrationListItem",
    "MigrationItem",
    # Constants
    "MigrationStatus",
    "Submarket",
    # Exceptions
    "VoltariumError",
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
]
