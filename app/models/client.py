from datetime import UTC, datetime
from typing import Any


def build_client_document(payload: dict[str, Any]) -> dict[str, Any]:
    now = datetime.now(UTC)
    return {
        **payload,
        "cli_email": payload.get("cli_email", "").lower() or None,
        "createdAt": now,
        "updatedAt": now,
    }
