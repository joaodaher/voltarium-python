"""Token model for OAuth2 authentication."""

import time
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    """OAuth2 token response model."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    access_token: str
    expires_in: int
    token_type: Literal["Bearer"]
    scope: str = ""
    refresh_expires_in: int = 0
    not_before_policy: int = Field(default=0, alias="not-before-policy")
    created_at: float = Field(default_factory=time.time)

    @property
    def expires_at(self) -> float:
        """Token expiration timestamp (computed once from creation time)."""
        return self.created_at + self.expires_in
