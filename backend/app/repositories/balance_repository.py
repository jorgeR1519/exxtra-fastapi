from app.db.collections import Collections
from app.repositories.base_repository import BaseRepository


class BalanceRepository(BaseRepository):
    collection_name = Collections.SALDOS

    def list_risk_credits(self, *, limit: int = 10) -> list[dict]:
        cursor = (
            self.collection.find(
                {},
                {
                    "_id": 0,
                    "credito": 1,
                    "cliente": 1,
                    "identificacion": 1,
                    "poliza": 1,
                    "placa": 1,
                    "estado": 1,
                    "mora": 1,
                    "dias_mora": 1,
                    "pagare": 1,
                    "cli_cedula": 1,
                    "numpoliza": 1,
                },
            )
            .sort([("mora", -1), ("dias_mora", -1)])
            .limit(limit)
        )

        items: list[dict] = []
        for document in cursor:
            items.append(
                {
                    "credito": str(document.get("credito") or document.get("pagare") or ""),
                    "cliente": str(document.get("cliente") or "Sin nombre"),
                    "identificacion": str(document.get("identificacion") or document.get("cli_cedula") or ""),
                    "poliza": str(document.get("poliza") or document.get("numpoliza") or ""),
                    "placa": str(document.get("placa") or ""),
                    "estado": str(document.get("estado") or "Seguimiento"),
                    "mora": int(document.get("mora") or document.get("dias_mora") or 0),
                }
            )
        return items
