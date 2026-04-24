from pydantic import BaseModel


class AdvisorDashboardSummary(BaseModel):
    pending_requests: int
    to_legalize_requests: int
    legalized_requests: int
    active_credits: int


class AdvisorRiskCreditItem(BaseModel):
    credito: str
    cliente: str
    identificacion: str
    poliza: str
    placa: str
    estado: str
    mora: int


class AdvisorDashboardResponse(BaseModel):
    summary: AdvisorDashboardSummary
    risk_credits: list[AdvisorRiskCreditItem]
