from app.repositories.balance_repository import BalanceRepository
from app.repositories.credit_request_repository import CreditRequestRepository
from app.repositories.new_business_repository import NewBusinessRepository
from app.schemas.credit_request import AdvisorDashboardResponse, AdvisorDashboardSummary, AdvisorRiskCreditItem


class CreditRequestService:
    def __init__(self) -> None:
        self.credit_request_repository = CreditRequestRepository()
        self.new_business_repository = NewBusinessRepository()
        self.balance_repository = BalanceRepository()

    def get_advisor_dashboard(self) -> AdvisorDashboardResponse:
        summary = AdvisorDashboardSummary(
            pending_requests=self.credit_request_repository.count_pending(),
            to_legalize_requests=self.credit_request_repository.count_to_legalize(),
            legalized_requests=self.credit_request_repository.count_by_estado_credito("L"),
            active_credits=self.new_business_repository.count_active(),
        )

        risk_credits = [
            AdvisorRiskCreditItem.model_validate(item)
            for item in self.balance_repository.list_risk_credits(limit=10)
        ]
        return AdvisorDashboardResponse(summary=summary, risk_credits=risk_credits)
