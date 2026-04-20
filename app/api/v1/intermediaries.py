from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_current_user
from app.schemas.intermediary import (
    IntermediaryCreate,
    IntermediaryListResponse,
    IntermediaryRelationsResponse,
    IntermediaryResponse,
    IntermediaryUpdate,
)
from app.services.intermediary_service import IntermediaryService

router = APIRouter()


@router.get("/intermediarios", response_model=IntermediaryListResponse)
def list_intermediaries(
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=200),
    _: dict = Depends(get_current_user),
) -> IntermediaryListResponse:
    return IntermediaryService().list_intermediaries(search=search, page=page, limit=limit)


@router.get("/intermediario/{intermediary_id}", response_model=IntermediaryResponse)
def get_intermediary(
    intermediary_id: str,
    _: dict = Depends(get_current_user),
) -> IntermediaryResponse:
    return IntermediaryService().get_intermediary(intermediary_id)


@router.get("/intermediario/{intermediary_id}/relaciones", response_model=IntermediaryRelationsResponse)
def get_intermediary_relations(
    intermediary_id: str,
    _: dict = Depends(get_current_user),
) -> IntermediaryRelationsResponse:
    return IntermediaryService().get_relations(intermediary_id)


@router.post("/nuevo-intermediario", response_model=IntermediaryResponse, status_code=status.HTTP_201_CREATED)
def create_intermediary(
    payload: IntermediaryCreate,
    _: dict = Depends(get_current_user),
) -> IntermediaryResponse:
    return IntermediaryService().create_intermediary(payload)


@router.put("/actualiza-intermediario/{intermediary_id}", response_model=IntermediaryResponse)
def update_intermediary(
    intermediary_id: str,
    payload: IntermediaryUpdate,
    _: dict = Depends(get_current_user),
) -> IntermediaryResponse:
    return IntermediaryService().update_intermediary(intermediary_id, payload)


@router.delete("/intermediario/{intermediary_id}")
def delete_intermediary(
    intermediary_id: str,
    _: dict = Depends(get_current_user),
) -> dict[str, str]:
    return IntermediaryService().delete_intermediary(intermediary_id)
