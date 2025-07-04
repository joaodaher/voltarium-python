"""CCEE sandbox agent credentials models."""

from dataclasses import dataclass


@dataclass
class SandboxAgentCredentials:
    """Credentials for a CCEE agent (Varejista or Concessionaria)."""

    client_id: str
    client_secret: str
    agent_code: int
    profiles: list[int]
