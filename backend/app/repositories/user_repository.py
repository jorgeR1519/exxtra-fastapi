from datetime import UTC, datetime

from bson import ObjectId

from app.db.collections import Collections
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    collection_name = Collections.USUARIOS

    def __init__(self) -> None:
        super().__init__()
        self.collection.create_index([("email", 1), ("tipo", 1)], unique=True)
        self.collection.create_index([("idUsuario", 1)], unique=True)

    def list(self, *, search: str | None = None, skip: int = 0, limit: int = 100) -> tuple[list[dict], int]:
        query: dict = {}
        if search:
            query["$or"] = [
                {"idUsuario": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}},
                {"tipo": {"$regex": search, "$options": "i"}},
                {"nombre": {"$regex": search, "$options": "i"}},
            ]

        cursor = self.collection.find(query).sort("createdAt", -1).skip(skip).limit(limit)
        total = self.collection.count_documents(query)
        return [self._serialize(document) for document in cursor], total

    def get_by_email(self, email: str, tipo: str | None = None, *, include_password: bool = False) -> dict | None:
        query: dict = {"email": email.lower()}
        if tipo:
            query["tipo"] = tipo
        return self._serialize(self.collection.find_one(query), include_password=include_password)

    def get_by_usuario(self, id_usuario: str, *, include_password: bool = False) -> dict | None:
        return self._serialize(
            self.collection.find_one({"idUsuario": id_usuario}),
            include_password=include_password,
        )

    def get_by_id(self, user_id: str, *, include_password: bool = False) -> dict | None:
        if not ObjectId.is_valid(user_id):
            return None
        return self._serialize(
            self.collection.find_one({"_id": ObjectId(user_id)}),
            include_password=include_password,
        )

    def create(self, user_data: dict) -> dict:
        result = self.collection.insert_one(user_data)
        return self.get_by_id(str(result.inserted_id))

    def update(self, user_id: str, data: dict) -> dict | None:
        if not ObjectId.is_valid(user_id):
            return None
        data["updatedAt"] = datetime.now(UTC)
        self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})
        return self.get_by_id(user_id)

    def delete(self, user_id: str) -> bool:
        if not ObjectId.is_valid(user_id):
            return False
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

    @staticmethod
    def _serialize(document: dict | None, *, include_password: bool = False) -> dict | None:
        if document is None:
            return None
        document["id"] = str(document.pop("_id"))
        if not include_password:
            document.pop("contrasena", None)
        return document
