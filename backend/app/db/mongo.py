from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.core.config import get_settings

_client: MongoClient | None = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        settings = get_settings()
        _client = MongoClient(settings.mongodb_uri)
    return _client


def get_database() -> Database:
    settings = get_settings()
    return get_client()[settings.mongodb_db_name]


def get_collection(name: str) -> Collection:
    return get_database()[name]
