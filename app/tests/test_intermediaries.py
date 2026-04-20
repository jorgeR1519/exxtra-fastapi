from datetime import UTC, datetime

from app.core.exceptions import AppException
from app.schemas.intermediary import IntermediaryCreate, IntermediaryUpdate
from app.services.intermediary_service import IntermediaryService


def _sample_intermediary() -> dict:
    return {
        "id": "507f1f77bcf86cd799439011",
        "int_nit": "900809703",
        "int_nombre": "MAKRO SEGUROS DE OCCIDENTE AA LTDA",
        "int_email": "contabilidad@exxtra.com.co",
        "int_ciudad": "76001",
        "int_cel": "3127873758",
        "int_tel": "3127873",
        "fecha": "Thu Aug 01 2024 00:00:00 GMT-0500 (Colombia Standard Time)",
        "createdAt": datetime.now(UTC),
        "updatedAt": datetime.now(UTC),
    }


def test_create_intermediary_success(monkeypatch) -> None:
    service = IntermediaryService()
    payload = IntermediaryCreate(
        int_nit="900809703",
        int_nombre="MAKRO SEGUROS DE OCCIDENTE AA LTDA",
        int_email="contabilidad@exxtra.com.co",
        int_ciudad="76001",
        int_cel="3127873758",
        int_tel="3127873",
    )

    monkeypatch.setattr(service.intermediary_repository, "get_by_nit", lambda _: None)
    monkeypatch.setattr(service.intermediary_repository, "create", lambda data: {**_sample_intermediary(), **data})

    result = service.create_intermediary(payload)

    assert result.int_nit == "900809703"
    assert result.int_email == "contabilidad@exxtra.com.co"


def test_create_intermediary_duplicate_nit(monkeypatch) -> None:
    service = IntermediaryService()
    payload = IntermediaryCreate(
        int_nit="900809703",
        int_nombre="MAKRO SEGUROS DE OCCIDENTE AA LTDA",
    )

    monkeypatch.setattr(service.intermediary_repository, "get_by_nit", lambda _: _sample_intermediary())

    try:
        service.create_intermediary(payload)
    except AppException as exc:
        assert exc.status_code == 409
        assert "NIT" in exc.detail
    else:
        raise AssertionError("Expected AppException for duplicate intermediary.")


def test_update_intermediary_success(monkeypatch) -> None:
    service = IntermediaryService()
    payload = IntermediaryUpdate(int_nombre="PRUEBAS INTERMEDIARIOS")

    monkeypatch.setattr(service.intermediary_repository, "get_by_id", lambda _: _sample_intermediary())
    monkeypatch.setattr(
        service.intermediary_repository,
        "update",
        lambda _, data: {**_sample_intermediary(), **data},
    )

    result = service.update_intermediary("507f1f77bcf86cd799439011", payload)

    assert result.int_nombre == "PRUEBAS INTERMEDIARIOS"


def test_get_intermediary_relations(monkeypatch) -> None:
    service = IntermediaryService()

    monkeypatch.setattr(service.intermediary_repository, "get_by_id", lambda _: _sample_intermediary())
    monkeypatch.setattr(
        service.intermediary_repository,
        "get_related_users",
        lambda _: [
            {
                "id": "507f1f77bcf86cd799439012",
                "idUsuario": "900809703",
                "email": "contabilidad@exxtra.com.co",
                "tipo": "intermediario",
                "primeravez": "no",
                "permisos": None,
                "createdAt": datetime.now(UTC),
                "updatedAt": datetime.now(UTC),
            }
        ],
    )
    monkeypatch.setattr(service.intermediary_repository, "count_related_new_business", lambda _: 3)

    result = service.get_relations("507f1f77bcf86cd799439011")

    assert result.intermediary.int_nit == "900809703"
    assert result.related_new_business_count == 3
    assert len(result.linked_users) == 1
