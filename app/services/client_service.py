from fastapi import status

from app.core.exceptions import AppException
from app.models.client import build_client_document
from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreate, ClientListResponse, ClientResponse, ClientUpdate


class ClientService:
    def __init__(self) -> None:
        self.client_repository = ClientRepository()

    def list_clients(self, *, search: str | None = None, page: int = 1, limit: int = 50) -> ClientListResponse:
        skip = (page - 1) * limit
        clients, total = self.client_repository.list(search=search, skip=skip, limit=limit)
        return ClientListResponse(
            data=[ClientResponse.model_validate(client) for client in clients],
            total=total,
        )

    def get_client(self, client_id: str) -> ClientResponse:
        client = self.client_repository.get_by_id(client_id)
        if not client:
            raise AppException("Cliente no encontrado.", status.HTTP_404_NOT_FOUND)
        return ClientResponse.model_validate(client)

    def create_client(self, payload: ClientCreate) -> ClientResponse:
        existing_client = self.client_repository.get_by_cedula(payload.cli_cedula)
        if existing_client:
            raise AppException("Ya existe un cliente con esa cédula.", status.HTTP_409_CONFLICT)

        client = self.client_repository.create(build_client_document(payload.model_dump()))
        return ClientResponse.model_validate(client)

    def update_client(self, client_id: str, payload: ClientUpdate) -> ClientResponse:
        current_client = self.client_repository.get_by_id(client_id)
        if not current_client:
            raise AppException("Cliente no encontrado.", status.HTTP_404_NOT_FOUND)

        update_data = payload.model_dump(exclude_none=True)
        updated_client = self.client_repository.update(client_id, update_data)
        if not updated_client:
            raise AppException("No fue posible actualizar el cliente.", status.HTTP_400_BAD_REQUEST)

        return ClientResponse.model_validate(updated_client)

    def delete_client(self, client_id: str) -> dict[str, str]:
        deleted = self.client_repository.delete(client_id)
        if not deleted:
            raise AppException("Cliente no encontrado.", status.HTTP_404_NOT_FOUND)
        return {"message": "Cliente eliminado correctamente."}
