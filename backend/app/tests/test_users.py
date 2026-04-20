from datetime import UTC, datetime

from app.core.exceptions import AppException
from app.schemas.user import UserCreateRequest, UserUpdateRequest
from app.services.user_service import UserService


def _sample_user() -> dict:
    return {
        "id": "507f1f77bcf86cd799439013",
        "idUsuario": "JOR002",
        "email": "admin@test.com",
        "tipo": "administrador",
        "nombre": "Administrador General",
        "primeravez": "si",
        "permisos": {"gestionarUsuarios": True},
        "activo": True,
        "verificado": True,
        "createdAt": datetime.now(UTC),
        "updatedAt": datetime.now(UTC),
    }


def test_create_user_success(monkeypatch) -> None:
    service = UserService()
    payload = UserCreateRequest(
        idUsuario="JOR002",
        email="admin@test.com",
        contrasena="123456",
        tipo="administrador",
        nombre="Administrador General",
    )

    monkeypatch.setattr(service.user_repository, "get_by_email", lambda *args, **kwargs: None)
    monkeypatch.setattr(service.user_repository, "get_by_usuario", lambda *args, **kwargs: None)
    monkeypatch.setattr(service.user_repository, "create", lambda data: {**_sample_user(), **data})

    result = service.create_user(payload)

    assert result.idUsuario == "JOR002"
    assert result.email == "admin@test.com"


def test_update_user_success(monkeypatch) -> None:
    service = UserService()
    payload = UserUpdateRequest(nombre="Admin Principal", activo=True)

    monkeypatch.setattr(service.user_repository, "get_by_id", lambda *args, **kwargs: _sample_user())
    monkeypatch.setattr(service.user_repository, "get_by_email", lambda *args, **kwargs: None)
    monkeypatch.setattr(service.user_repository, "update", lambda *args, **kwargs: {**_sample_user(), "nombre": "Admin Principal"})

    result = service.update_user("507f1f77bcf86cd799439013", payload)

    assert result.nombre == "Admin Principal"


def test_delete_user_self_blocked() -> None:
    service = UserService()

    try:
        service.delete_user("507f1f77bcf86cd799439013", "507f1f77bcf86cd799439013")
    except AppException as exc:
        assert exc.status_code == 400
        assert "propio usuario" in exc.detail
    else:
        raise AssertionError("Expected AppException when deleting the current admin user.")
