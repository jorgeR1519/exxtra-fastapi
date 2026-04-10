from pymongo.collection import Collection

from app.db.mongo import get_collection


class BaseRepository:
    collection_name: str = ""

    def __init__(self) -> None:
        if not self.collection_name:
            raise ValueError("collection_name must be defined in the repository.")
        self.collection: Collection = get_collection(self.collection_name)
