from datetime import UTC, datetime

from bson import ObjectId

from app.db.collections import Collections
from app.repositories.base_repository import BaseRepository


class ClientRepository(BaseRepository):
    collection_name = Collections.CLIENTES

    def __init__(self) -> None:
        super().__init__()
        self.collection.create_index([("cli_cedula", 1)], unique=True)

    def list(self, *, search: str | None = None, skip: int = 0, limit: int = 100) -> tuple[list[dict], int]:
        query: dict = {}
        if search:
            query["$or"] = [
                {"cli_cedula": {"$regex": search, "$options": "i"}},
                {"cli_nombre": {"$regex": search, "$options": "i"}},
                {"cli_email": {"$regex": search, "$options": "i"}},
            ]

        cursor = self.collection.find(query).sort("createdAt", -1).skip(skip).limit(limit)
        total = self.collection.count_documents(query)
        return [self._serialize(document) for document in cursor], total

    def get_by_id(self, client_id: str) -> dict | None:
        if not ObjectId.is_valid(client_id):
            return None
        return self._serialize(self.collection.find_one({"_id": ObjectId(client_id)}))

    def get_by_cedula(self, cli_cedula: str) -> dict | None:
        return self._serialize(self.collection.find_one({"cli_cedula": cli_cedula}))

    def create(self, data: dict) -> dict:
        result = self.collection.insert_one(data)
        return self.get_by_id(str(result.inserted_id))

    def update(self, client_id: str, data: dict) -> dict | None:
        if not ObjectId.is_valid(client_id):
            return None
        data["updatedAt"] = datetime.now(UTC)
        self.collection.update_one({"_id": ObjectId(client_id)}, {"$set": data})
        return self.get_by_id(client_id)

    def delete(self, client_id: str) -> bool:
        if not ObjectId.is_valid(client_id):
            return False
        result = self.collection.delete_one({"_id": ObjectId(client_id)})
        return result.deleted_count > 0

    @staticmethod
    def _serialize(document: dict | None) -> dict | None:
        if document is None:
            return None
        document["id"] = str(document.pop("_id"))
        return document
