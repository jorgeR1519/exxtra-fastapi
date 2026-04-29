from fastapi.testclient import TestClient

from app.api.deps import get_current_user
from app.main import app
from app.services.credit_request_service import CreditRequestService


def test_advisor_dashboard_endpoint(monkeypatch) -> None:
    def fake_dashboard(self) -> dict:
        return {
            "summary": {
                "pending_requests": 3,
                "to_legalize_requests": 1,
                "legalized_requests": 2,
                "active_credits": 5,
            },
            "risk_credits": [],
        }

    app.dependency_overrides[get_current_user] = lambda: {"id": "user-1", "tipo": "asesor"}
    monkeypatch.setattr(CreditRequestService, "get_advisor_dashboard", fake_dashboard)

    client = TestClient(app)
    response = client.get("/api/v1/asesores/dashboard")

    assert response.status_code == 200
    assert response.json()["summary"]["pending_requests"] == 3

    app.dependency_overrides.clear()


def test_list_credit_requests_endpoint(monkeypatch) -> None:
    def fake_list(self, *, current_user: dict, search: str | None, page: int, limit: int) -> dict:
        return {
            "data": [
                {
                    "id": "req-1",
                    "cli_cedula": "123",
                    "pagare": 20001,
                    "credito": "20001",
                    "estado_credito": "p",
                }
            ],
            "total": 1,
        }

    app.dependency_overrides[get_current_user] = lambda: {"id": "user-1", "tipo": "asesor", "idUsuario": "ASE001"}
    monkeypatch.setattr(CreditRequestService, "list_credit_requests", fake_list)

    client = TestClient(app)
    response = client.get("/api/v1/solicitudes-de-creditos?page=1&limit=20&search=20001")

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["data"][0]["credito"] == "20001"

    app.dependency_overrides.clear()


def test_create_credit_request_endpoint(monkeypatch) -> None:
    def fake_create(self, payload, *, current_user: dict) -> dict:
        return {
            "id": "req-2",
            "cli_cedula": payload.cli_cedula,
            "pagare": 20002,
            "credito": "20002",
            "ase_ced": current_user["idUsuario"],
        }

    app.dependency_overrides[get_current_user] = lambda: {"id": "user-1", "tipo": "asesor", "idUsuario": "ASE001"}
    monkeypatch.setattr(CreditRequestService, "create_credit_request", fake_create)

    client = TestClient(app)
    response = client.post("/api/v1/solicitud-de-credito", json={"cli_cedula": "900123456"})

    assert response.status_code == 201
    assert response.json()["pagare"] == 20002
    assert response.json()["ase_ced"] == "ASE001"

    app.dependency_overrides.clear()
