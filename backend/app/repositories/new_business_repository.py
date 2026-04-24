from app.db.collections import Collections
from app.repositories.base_repository import BaseRepository


class NewBusinessRepository(BaseRepository):
    collection_name = Collections.NEGOCIOS_NUEVOS

    def count_active(self) -> int:
        return self.collection.count_documents({})
