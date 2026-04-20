from datetime import UTC, datetime
from typing import Any

from app.core.security import hash_password


def build_user_document(
    *,
    id_usuario: str,
    email: str,
    contrasena: str,
    tipo: str,
    primeravez: str = "si",
    permisos: dict[str, bool] | None = None,
) -> dict[str, Any]:
    now = datetime.now(UTC)
    return {
        "idUsuario": id_usuario,
        "email": email.lower(),
        "contrasena": hash_password(contrasena),
        "tipo": tipo,
        "primeravez": primeravez,
        "permisos": permisos,
        "createdAt": now,
        "updatedAt": now,
    }
