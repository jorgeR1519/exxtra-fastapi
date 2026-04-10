from datetime import UTC, datetime

from bson import ObjectId

from app.db.collections import Collections
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    collection_name = Collections.USUARIOS

    def __init__(self) -> None:
        super().__init__()
        self.collection.create_index([("email", 1), ("tipo", 1)], unique=True)

    def get_by_email(self, email: str, tipo: str | None = None) -> dict | None:
        query: dict = {"email": email.lower()}
        if tipo:
            query["tipo"] = tipo
        return self._serialize(self.collection.find_one(query))

    def get_by_usuario(self, id_usuario: str) -> dict | None:
        return self._serialize(self.collection.find_one({"idUsuario": id_usuario}))

    def get_by_id(self, user_id: str) -> dict | None:
        if not ObjectId.is_valid(user_id):
            return None
        return self._serialize(self.collection.find_one({"_id": ObjectId(user_id)}))

    def create(self, user_data: dict) -> dict:
        result = self.collection.insert_one(user_data)
        return self.get_by_id(str(result.inserted_id))

    def update_password(self, user_id: str, hashed_password: str) -> dict | None:
        self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"contrasena": hashed_password, "updatedAt": datetime.now(UTC)}},
        )
        return self.get_by_id(user_id)

    @staticmethod
    def _serialize(document: dict | None) -> dict | None:
        if document is None:
            return None
        document["id"] = str(document.pop("_id"))
        return document
