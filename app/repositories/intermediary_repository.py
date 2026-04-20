from datetime import UTC, datetime

from bson import ObjectId

from app.db.collections import Collections
from app.db.mongo import get_collection
from app.repositories.base_repository import BaseRepository


class IntermediaryRepository(BaseRepository):
    collection_name = Collections.INTERMEDIARIOS

    def __init__(self) -> None:
        super().__init__()
        self.collection.create_index([("int_nit", 1)], unique=True)
        self.user_collection = get_collection(Collections.USUARIOS)
        self.new_business_collection = get_collection(Collections.NEGOCIOS_NUEVOS)

    def list(self, *, search: str | None = None, skip: int = 0, limit: int = 100) -> tuple[list[dict], int]:
        query: dict = {}
        if search:
            query["$or"] = [
                {"int_nit": {"$regex": search, "$options": "i"}},
                {"int_nombre": {"$regex": search, "$options": "i"}},
                {"int_email": {"$regex": search, "$options": "i"}},
                {"int_ciudad": {"$regex": search, "$options": "i"}},
            ]

        cursor = self.collection.find(query).sort("createdAt", -1).skip(skip).limit(limit)
        total = self.collection.count_documents(query)
        return [self._serialize(document) for document in cursor], total

    def get_by_id(self, intermediary_id: str) -> dict | None:
        if not ObjectId.is_valid(intermediary_id):
            return None
        return self._serialize(self.collection.find_one({"_id": ObjectId(intermediary_id)}))

    def get_by_nit(self, int_nit: str) -> dict | None:
        return self._serialize(self.collection.find_one({"int_nit": int_nit}))

    def create(self, data: dict) -> dict:
        result = self.collection.insert_one(data)
        return self.get_by_id(str(result.inserted_id))

    def update(self, intermediary_id: str, data: dict) -> dict | None:
        if not ObjectId.is_valid(intermediary_id):
            return None
        data["updatedAt"] = datetime.now(UTC)
        self.collection.update_one({"_id": ObjectId(intermediary_id)}, {"$set": data})
        return self.get_by_id(intermediary_id)

    def delete(self, intermediary_id: str) -> bool:
        if not ObjectId.is_valid(intermediary_id):
            return False
        result = self.collection.delete_one({"_id": ObjectId(intermediary_id)})
        return result.deleted_count > 0

    def get_related_users(self, int_nit: str) -> list[dict]:
        cursor = self.user_collection.find({"idUsuario": int_nit})
        return [self._serialize(document) for document in cursor]

    def count_related_new_business(self, int_nit: str) -> int:
        return self.new_business_collection.count_documents({"int_nit": int_nit})

    @staticmethod
    def _serialize(document: dict | None) -> dict | None:
        if document is None:
            return None
        document["id"] = str(document.pop("_id"))
        return document
