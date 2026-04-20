from datetime import UTC, datetime
from typing import Any


def build_intermediary_document(payload: dict[str, Any]) -> dict[str, Any]:
    now = datetime.now(UTC)
    return {
        **payload,
        "int_email": payload.get("int_email", "").lower() or None,
        "createdAt": now,
        "updatedAt": now,
    }
