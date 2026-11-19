import os
import tempfile
from pathlib import Path

import pytest

_tmp = Path(tempfile.mkdtemp()) / "test.db"
os.environ["CREDISTEP_DB_URL"] = f"sqlite:///{_tmp.as_posix()}"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


def auth_headers(client, email="nuevo@test.co", password="clave-segura-1", **extra):
    r = client.post("/api/auth/register", json={"name": "Usuario Test", "email": email, "password": password, **extra})
    if r.status_code == 409:
        r = client.post("/api/auth/login", json={"email": email, "password": password})
    assert r.status_code in (200, 201), r.text
    return {"Authorization": f"Bearer {r.json()['token']}"}


@pytest.fixture
def headers(client, request):
    return auth_headers(client, email=f"{request.node.name[:40]}@test.co")
