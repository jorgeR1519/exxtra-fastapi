from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_current_user
from app.schemas.client import ClientCreate, ClientListResponse, ClientResponse, ClientUpdate
from app.services.client_service import ClientService

router = APIRouter()


@router.get("/clientes", response_model=ClientListResponse)
def list_clients(
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=200),
    _: dict = Depends(get_current_user),
) -> ClientListResponse:
    return ClientService().list_clients(search=search, page=page, limit=limit)


@router.get("/cliente/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: str,
    _: dict = Depends(get_current_user),
) -> ClientResponse:
    return ClientService().get_client(client_id)


@router.post("/nuevo-cliente", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    payload: ClientCreate,
    _: dict = Depends(get_current_user),
) -> ClientResponse:
    return ClientService().create_client(payload)


@router.put("/actualiza-cliente/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: str,
    payload: ClientUpdate,
    _: dict = Depends(get_current_user),
) -> ClientResponse:
    return ClientService().update_client(client_id, payload)


@router.delete("/cliente/{client_id}")
def delete_client(
    client_id: str,
    _: dict = Depends(get_current_user),
) -> dict[str, str]:
    return ClientService().delete_client(client_id)
