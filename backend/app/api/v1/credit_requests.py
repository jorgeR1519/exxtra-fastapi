from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.schemas.credit_request import AdvisorDashboardResponse
from app.services.credit_request_service import CreditRequestService

router = APIRouter()


@router.get("/asesores/dashboard", response_model=AdvisorDashboardResponse)
def get_advisor_dashboard(_: dict = Depends(get_current_user)) -> AdvisorDashboardResponse:
    return CreditRequestService().get_advisor_dashboard()
