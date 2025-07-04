"""Voltarium: Asynchronous Python client for CCEE API.

This package provides an asynchronous Python client for the CCEE
(Brazilian Electric Energy Commercialization Chamber) API.
"""

__version__ = "0.1.0"
__author__ = "joaodaher"
__email__ = "joaodaher@example.com"

from .client import (
    CreateMigrationRequest,
    MigrationItem,
    MigrationListItem,
    Token,
    UpdateMigrationRequest,
    VoltariumClient,
)
from .exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
    VoltariumError,
)

__all__ = [
    # Client
    "VoltariumClient",
    # Models
    "Token",
    "CreateMigrationRequest",
    "UpdateMigrationRequest",
    "MigrationListItem",
    "MigrationItem",
    # Exceptions
    "VoltariumError",
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
]
