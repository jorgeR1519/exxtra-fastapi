from datetime import UTC, datetime

from bson import ObjectId

from app.core.exceptions import AppException
from app.db.collections import Collections
from app.repositories.base_repository import BaseRepository


class CreditRequestRepository(BaseRepository):
    collection_name = Collections.SOLICITUD_DE_CREDITO

    def list(
        self,
        *,
        query: dict | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[list[dict], int]:
        query = query or {}
        cursor = self.collection.find(query).sort("createdAt", -1).skip(skip).limit(limit)
        total = self.collection.count_documents(query)
        return [self._serialize(document) for document in cursor], total

    def get_by_id(self, request_id: str) -> dict | None:
        if not ObjectId.is_valid(request_id):
            return None
        return self._serialize(self.collection.find_one({"_id": ObjectId(request_id)}))

    def create(self, payload: dict) -> dict:
        now = datetime.now(UTC)
        document = dict(payload)
        if not document.get("pagare"):
            document["pagare"] = self._get_next_pagare()
        document.setdefault("credito", str(document["pagare"]))
        document.setdefault("estado_credito", "p")
        document.setdefault("createdAt", now)
        document["updatedAt"] = now

        result = self.collection.insert_one(document)
        created = self.get_by_id(str(result.inserted_id))
        if created is None:
            raise AppException(detail="No fue posible crear la solicitud.")
        return created

    def update(self, request_id: str, payload: dict) -> dict | None:
        if not ObjectId.is_valid(request_id):
            return None

        data = dict(payload)
        data["updatedAt"] = datetime.now(UTC)
        self.collection.update_one({"_id": ObjectId(request_id)}, {"$set": data})
        return self.get_by_id(request_id)

    def count_by_estado_credito(self, estado_credito: str) -> int:
        return self.collection.count_documents({"estado_credito": estado_credito})

    def count_pending(self) -> int:
        return self.collection.count_documents({"estado_credito": {"$ne": "L"}})

    def count_to_legalize(self) -> int:
        return self.collection.count_documents(
            {
                "estado_credito": {"$ne": "L"},
                "estado": {"$in": ["Documentos Adjuntos", "Pago CI"]},
            }
        )

    def build_search_query(self, search: str | None = None) -> dict:
        if not search:
            return {}

        value = search.strip()
        if not value:
            return {}

        pagare = int(value) if value.isdigit() else None
        conditions: list[dict] = [
            {"placa": {"$regex": value, "$options": "i"}},
            {"numpoliza": {"$regex": value, "$options": "i"}},
            {"cli_cedula": {"$regex": value, "$options": "i"}},
        ]
        if pagare is not None:
            conditions.insert(0, {"pagare": pagare})

        return {"$or": conditions}

    def build_ready_to_legalize_query(self) -> dict:
        return {
            "estado_credito": "p",
            "soli_diligenciada": "si",
            "soli_firmada": "si",
            "soli_documentos": "si",
            "$or": [{"soli_pagada": "si"}, {"aut_conta": "SI"}],
        }

    def _get_next_pagare(self) -> int:
        last_document = self.collection.find_one({}, sort=[("pagare", -1)], projection={"pagare": 1})
        last_pagare = int(last_document.get("pagare") or 19999) if last_document else 19999
        return last_pagare + 1

    @staticmethod
    def _serialize(document: dict | None) -> dict | None:
        if document is None:
            return None
        document["id"] = str(document.pop("_id"))
        return document
