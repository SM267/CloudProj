from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "CloudProj"}


def test_meta() -> None:
    response = client.get("/api/v1/meta")
    assert response.status_code == 200
    assert response.json()["name"] == "CloudProj"


def test_factory_plan() -> None:
    response = client.post(
        "/api/v1/factory/plan",
        json={
            "requirement": "Build a task management REST API with authentication and PostgreSQL",
            "language": "python",
            "framework": "fastapi",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["language"] == "python"
    assert body["architecture"]["provider_neutral"] is True
    assert len(body["stages"]) == 6


def test_factory_rejects_short_requirement() -> None:
    response = client.post("/api/v1/factory/plan", json={"requirement": "short"})
    assert response.status_code == 422
