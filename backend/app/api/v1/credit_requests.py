from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_current_user
from app.schemas.credit_request import (
    AdvisorDashboardResponse,
    CreditRequestCreate,
    CreditRequestDetailResponse,
    CreditRequestListResponse,
    CreditRequestResponse,
    CreditRequestUpdate,
)
from app.services.credit_request_service import CreditRequestService

router = APIRouter()


@router.get("/asesores/dashboard", response_model=AdvisorDashboardResponse)
def get_advisor_dashboard(_: dict = Depends(get_current_user)) -> AdvisorDashboardResponse:
    return CreditRequestService().get_advisor_dashboard()


@router.get("/solicitudes-de-creditos", response_model=CreditRequestListResponse)
def list_credit_requests(
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=200),
    current_user: dict = Depends(get_current_user),
) -> CreditRequestListResponse:
    return CreditRequestService().list_credit_requests(
        current_user=current_user,
        search=search,
        page=page,
        limit=limit,
    )


@router.get("/solicitudes-de-creditos/estado/{estado_credito}", response_model=CreditRequestListResponse)
def list_credit_requests_by_status(
    estado_credito: str,
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=200),
    current_user: dict = Depends(get_current_user),
) -> CreditRequestListResponse:
    return CreditRequestService().list_credit_requests_by_status(
        estado_credito=estado_credito,
        current_user=current_user,
        search=search,
        page=page,
        limit=limit,
    )


@router.get("/solicitudes-de-creditos/para-legalizar", response_model=CreditRequestListResponse)
def list_ready_to_legalize(
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=200),
    current_user: dict = Depends(get_current_user),
) -> CreditRequestListResponse:
    return CreditRequestService().list_ready_to_legalize(
        current_user=current_user,
        search=search,
        page=page,
        limit=limit,
    )


@router.get("/solicitud-de-credito", response_model=CreditRequestDetailResponse)
def get_credit_request(
    id: str = Query(..., min_length=1),
    _: dict = Depends(get_current_user),
) -> CreditRequestDetailResponse:
    return CreditRequestService().get_credit_request(id)


@router.post("/solicitud-de-credito", response_model=CreditRequestResponse, status_code=status.HTTP_201_CREATED)
def create_credit_request(
    payload: CreditRequestCreate,
    current_user: dict = Depends(get_current_user),
) -> CreditRequestResponse:
    return CreditRequestService().create_credit_request(payload, current_user=current_user)


@router.put("/solicitud-de-credito/{request_id}", response_model=CreditRequestResponse)
def update_credit_request(
    request_id: str,
    payload: CreditRequestUpdate,
    _: dict = Depends(get_current_user),
) -> CreditRequestResponse:
    return CreditRequestService().update_credit_request(request_id, payload)
