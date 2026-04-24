from app.db.collections import Collections
from app.repositories.base_repository import BaseRepository


class CreditRequestRepository(BaseRepository):
    collection_name = Collections.SOLICITUD_DE_CREDITO

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
