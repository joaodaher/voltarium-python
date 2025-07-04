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

    @property
    def expires_at(self) -> float:
        """Calculate token expiration timestamp."""
        return time.time() + self.expires_in
