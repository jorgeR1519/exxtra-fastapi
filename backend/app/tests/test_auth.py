from app.core.security import create_access_token, decode_access_token, hash_password, verify_password
from app.schemas.auth import LoginRequest
from app.services.auth_service import AuthService


def test_password_hashing_roundtrip() -> None:
    password = "super-secret-123"
    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password) is True


def test_access_token_roundtrip() -> None:
    token = create_access_token("user-id-1", "admin01", "administrador", "demo@example.com")
    payload = decode_access_token(token)

    assert payload["sub"] == "user-id-1"
    assert payload["usuario"] == "admin01"
    assert payload["tipo"] == "administrador"
    assert payload["email"] == "demo@example.com"


def test_login_requests_password_from_repository(monkeypatch) -> None:
    service = AuthService()
    hashed_password = hash_password("123456")
    captured: dict[str, object] = {}

    def fake_get_by_usuario(usuario: str, *, include_password: bool = False):
        captured["usuario"] = usuario
        captured["include_password"] = include_password
        return {
            "id": "user-id-1",
            "idUsuario": "JOR002",
            "email": "admin@test.com",
            "tipo": "administrador",
            "contrasena": hashed_password,
        }

    monkeypatch.setattr(service.user_repository, "get_by_usuario", fake_get_by_usuario)

    response = service.login(LoginRequest(usuario="JOR002", contrasena="123456"))

    assert captured["usuario"] == "JOR002"
    assert captured["include_password"] is True
    assert response.user.idUsuario == "JOR002"
