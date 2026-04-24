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
