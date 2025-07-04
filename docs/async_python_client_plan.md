```markdown
# Voltarium: Asynchronous Python 3.13 Client for CCEE API

This document outlines a detailed plan to build **Voltarium**, an **asynchronous Python 3.13** client for the CCEE (Brazilian Electric Energy Commercialization Chamber) API. Inspired by the [GitHub Python client](https://github.com/pygithub/PyGithub), Voltarium uses Astral UV and Ruff to deliver a modern, robust design.

---

## 🎯 1. Project Setup

1. **Tools & Layout**  
   - **Python 3.13**  
   - **Dependency & Packaging:** Astral UV  
   - **Linting & Formatting:** Ruff & Black  

2. **Directory Structure** (`voltarium` package):
```

├── pyproject.toml ├── README.md ├── src/ │   └── voltarium/ │       ├── **init**.py │       ├── auth.py │       ├── client.py │       ├── models.py │       ├── exceptions.py │       └── utils.py └── tests/ ├── conftest.py ├── test\_auth.py └── test\_migrations.py

````

3. **Key Configurations (pyproject.toml)**
```toml
[project]
name = "voltarium"
version = "0.1.0"
requires-python = ">=3.13"

[tool.astral]
# Build settings, package includes, entry points...

[tool.ruff]
line-length = 88
select = ["E", "W", "F", "I"]
````

---

## 🔐 2. Authentication Module (`auth.py`)

### 2.1 Pydantic Model for OAuth2 Token

```python
from pydantic import BaseModel
from typing import Literal

class TokenResponse(BaseModel):
    access_token: str
    expires_in: int
    token_type: Literal["Bearer"]
```

### 2.2 `AuthClient` Class Responsibilities

- **Constructor**: accepts `base_url`, `client_id`, `client_secret`.
- ``: POST `/oauth/token`, parse JSON into `TokenResponse`, cache token and expiry.
- ``: returns `{"Authorization": "Bearer <token>"}`, auto-refreshes if expired.
- **Retries**: use Tenacity for exponential backoff on transient errors.

### 2.3 Error Handling

- Define `AuthenticationError` in `exceptions.py`.
- Raise `AuthenticationError` for permanent 4xx/5xx responses.

---

## 📐 3. Data Models (`models.py`)

Define Pydantic schemas for the `` endpoints:

- ``
- ``
- ``
- ``
- ``

Use `Field(..., alias="camelCase")` for JSON field mapping.

---

## 🛠️ 4. Core HTTP Client (`client.py`)

### 4.1 `VoltariumClient` Implementation

```python
import httpx
from .auth import AuthClient

class VoltariumClient:
    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
    ) -> None:
        self._auth = AuthClient(base_url, client_id, client_secret)
        self._http = httpx.AsyncClient(base_url=base_url, timeout=30)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._http.aclose()

    async def _request(
        self, method: str, path: str, **kwargs
    ) -> dict:
        headers = await self._auth.get_auth_header()
        response = await self._http.request(method, path, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()
```

### 4.2 GitHub Client Style Patterns

- Chainable methods where appropriate
- Inline docstrings referencing Postman collection
- Shared utilities in `utils.py` (e.g., query builders)

---

## 🚚 5. “migracoes” Endpoints

Add these methods to `VoltariumClient`:

1. ``
2. ``
3. ``
4. ``

Implementation details:

- Input serialization: `.dict(exclude_none=True, by_alias=True)`
- Request call: `_request("HTTP_METHOD", "/migracoes/...", json=...)`
- Output parsing into Pydantic models

---

## 🧪 6. Automated Testing

- Use `pytest-asyncio` for async tests
- Mock HTTP using `httpx.MockTransport` in `conftest.py`
- Cover both success (2xx) and error (4xx/5xx) cases

**Example Fixture:**

```python
import pytest
from httpx import AsyncClient, Request, Response

@pytest.fixture
async def auth_client(monkeypatch):
    async def handler(request: Request) -> Response:
        return Response(
            status_code=200,
            json={"access_token": "token", "expires_in": 3600, "token_type": "Bearer"}
        )
    transport = httpx.MockTransport(handler)
    client = AsyncClient(transport=transport)
    monkeypatch.setattr("voltarium.auth.httpx.AsyncClient", lambda **kwargs: client)
    return client
```

---

## 📄 7. Documentation & Examples

- **README.md**:
  - **Installation**: `pip install .`
  - **Quickstart**:
    ```python
    import asyncio
    from voltarium import VoltariumClient, CreateMigrationRequest

    async def main():
        async with VoltariumClient(
            base_url="https://api.ccee.org.br",
            client_id="YOUR_ID",
            client_secret="YOUR_SECRET"
        ) as client:
            req = CreateMigrationRequest(
                codigoAgenteVarejista="123",
                codigoConcessionaria="456",
                codigoPerfil="789",
                # ... other fields
            )
            resp = await client.create_migration(req)
            print(resp.id_migracao)

    asyncio.run(main())
    ```
- Use Google/NumPy–style docstrings for Sphinx or mkdocstrings

---

## ⚙️ 8. CI/CD & Quality Gates

- **GitHub Actions**:
  - `ruff --fix`, `black --check`, `mypy`, `pytest`
- **Versioning**: Semantic Versioning; publish to PyPI on tags

---

## 📋 9. Tasks for Agentic LLM

```yaml
tasks:
  - id: init_project
    description: Initialize Voltarium repo with Astral UV & Ruff config
  - id: implement_auth
    description: Build AuthClient with token caching & retry logic
  - id: define_models
    description: Create Pydantic models for migrations
  - id: core_client
    description: Implement VoltariumClient core and _request wrapper
  - id: migracoes_endpoints
    description: Add create/list/get/update migration methods
  - id: testing
    description: Write async tests using pytest-asyncio and MockTransport
  - id: docs
    description: Complete README and add docstrings
  - id: ci
    description: Configure GitHub Actions pipeline
```

```
```
