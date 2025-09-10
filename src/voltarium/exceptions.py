"""Exception classes for Voltarium."""


class VoltariumError(Exception):
    """Base exception for all Voltarium-related errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AuthenticationError(VoltariumError):
    """Raised when authentication fails."""

    pass


class NotFoundError(VoltariumError):
    """Raised when a resource is not found (404)."""

    pass


class ValidationError(VoltariumError):
    """Raised when request validation fails (400)."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return f"Validation error: {self.code} - {self.message}"


class RateLimitError(VoltariumError):
    """Raised when rate limit is exceeded (429)."""

    pass


class ServerError(VoltariumError):
    """Raised when server returns 5xx error."""

    pass
