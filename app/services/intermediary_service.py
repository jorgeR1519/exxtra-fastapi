from fastapi import status

from app.core.exceptions import AppException
from app.models.intermediary import build_intermediary_document
from app.repositories.intermediary_repository import IntermediaryRepository
from app.schemas.intermediary import (
    IntermediaryCreate,
    IntermediaryListResponse,
    IntermediaryRelationsResponse,
    IntermediaryResponse,
    IntermediaryUpdate,
)
from app.schemas.user import UserResponse


class IntermediaryService:
    def __init__(self) -> None:
        self.intermediary_repository = IntermediaryRepository()

    def list_intermediaries(
        self, *, search: str | None = None, page: int = 1, limit: int = 50
    ) -> IntermediaryListResponse:
        skip = (page - 1) * limit
        intermediaries, total = self.intermediary_repository.list(search=search, skip=skip, limit=limit)
        return IntermediaryListResponse(
            data=[IntermediaryResponse.model_validate(intermediary) for intermediary in intermediaries],
            total=total,
        )

    def get_intermediary(self, intermediary_id: str) -> IntermediaryResponse:
        intermediary = self.intermediary_repository.get_by_id(intermediary_id)
        if not intermediary:
            raise AppException("Intermediario no encontrado.", status.HTTP_404_NOT_FOUND)
        return IntermediaryResponse.model_validate(intermediary)

    def create_intermediary(self, payload: IntermediaryCreate) -> IntermediaryResponse:
        existing_intermediary = self.intermediary_repository.get_by_nit(payload.int_nit)
        if existing_intermediary:
            raise AppException("Ya existe un intermediario con ese NIT.", status.HTTP_409_CONFLICT)

        intermediary = self.intermediary_repository.create(build_intermediary_document(payload.model_dump()))
        return IntermediaryResponse.model_validate(intermediary)

    def update_intermediary(self, intermediary_id: str, payload: IntermediaryUpdate) -> IntermediaryResponse:
        current_intermediary = self.intermediary_repository.get_by_id(intermediary_id)
        if not current_intermediary:
            raise AppException("Intermediario no encontrado.", status.HTTP_404_NOT_FOUND)

        update_data = payload.model_dump(exclude_none=True)
        updated_intermediary = self.intermediary_repository.update(intermediary_id, update_data)
        if not updated_intermediary:
            raise AppException("No fue posible actualizar el intermediario.", status.HTTP_400_BAD_REQUEST)

        return IntermediaryResponse.model_validate(updated_intermediary)

    def delete_intermediary(self, intermediary_id: str) -> dict[str, str]:
        deleted = self.intermediary_repository.delete(intermediary_id)
        if not deleted:
            raise AppException("Intermediario no encontrado.", status.HTTP_404_NOT_FOUND)
        return {"message": "Intermediario eliminado correctamente."}

    def get_relations(self, intermediary_id: str) -> IntermediaryRelationsResponse:
        intermediary = self.intermediary_repository.get_by_id(intermediary_id)
        if not intermediary:
            raise AppException("Intermediario no encontrado.", status.HTTP_404_NOT_FOUND)

        linked_users = self.intermediary_repository.get_related_users(intermediary["int_nit"])
        related_new_business_count = self.intermediary_repository.count_related_new_business(intermediary["int_nit"])

        return IntermediaryRelationsResponse(
            intermediary=IntermediaryResponse.model_validate(intermediary),
            linked_users=[UserResponse.model_validate(user) for user in linked_users],
            related_new_business_count=related_new_business_count,
        )
