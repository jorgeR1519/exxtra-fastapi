from fastapi import status

from app.core.exceptions import AppException
from app.repositories.balance_repository import BalanceRepository
from app.repositories.credit_request_repository import CreditRequestRepository
from app.repositories.new_business_repository import NewBusinessRepository
from app.schemas.credit_request import (
    AdvisorDashboardResponse,
    AdvisorDashboardSummary,
    AdvisorRiskCreditItem,
    CreditRequestCreate,
    CreditRequestDetailResponse,
    CreditRequestListResponse,
    CreditRequestResponse,
    CreditRequestUpdate,
)


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

    def list_credit_requests(
        self,
        *,
        current_user: dict,
        search: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> CreditRequestListResponse:
        query = self._build_access_query(current_user)
        query.update(self.credit_request_repository.build_search_query(search))
        items, total = self.credit_request_repository.list(
            query=query,
            skip=(page - 1) * limit,
            limit=limit,
        )
        return CreditRequestListResponse(
            data=[CreditRequestResponse.model_validate(item) for item in items],
            total=total,
        )

    def list_credit_requests_by_status(
        self,
        *,
        estado_credito: str,
        current_user: dict,
        search: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> CreditRequestListResponse:
        query = {"estado_credito": estado_credito, **self._build_access_query(current_user)}
        query.update(self.credit_request_repository.build_search_query(search))
        items, total = self.credit_request_repository.list(
            query=query,
            skip=(page - 1) * limit,
            limit=limit,
        )
        return CreditRequestListResponse(
            data=[CreditRequestResponse.model_validate(item) for item in items],
            total=total,
        )

    def list_ready_to_legalize(
        self,
        *,
        current_user: dict,
        search: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> CreditRequestListResponse:
        query = self.credit_request_repository.build_ready_to_legalize_query()
        query.update(self._build_access_query(current_user))
        query.update(self.credit_request_repository.build_search_query(search))
        items, total = self.credit_request_repository.list(
            query=query,
            skip=(page - 1) * limit,
            limit=limit,
        )
        return CreditRequestListResponse(
            data=[CreditRequestResponse.model_validate(item) for item in items],
            total=total,
        )

    def get_credit_request(self, request_id: str) -> CreditRequestDetailResponse:
        request = self.credit_request_repository.get_by_id(request_id)
        if request is None:
            raise AppException(detail="Solicitud no encontrada.", status_code=status.HTTP_404_NOT_FOUND)

        if request.get("archivos") and isinstance(request["archivos"], list):
            request["archivos"] = list(dict.fromkeys([item for item in request["archivos"] if item]))

        return CreditRequestDetailResponse.model_validate(request)

    def create_credit_request(self, payload: CreditRequestCreate, *, current_user: dict) -> CreditRequestResponse:
        data = payload.model_dump(exclude_none=True, by_alias=True)
        self._hydrate_actor_fields(data, current_user)
        created = self.credit_request_repository.create(data)
        return CreditRequestResponse.model_validate(created)

    def update_credit_request(self, request_id: str, payload: CreditRequestUpdate) -> CreditRequestResponse:
        data = payload.model_dump(exclude_none=True, by_alias=True)
        updated = self.credit_request_repository.update(request_id, data)
        if updated is None:
            raise AppException(detail="Solicitud no encontrada.", status_code=status.HTTP_404_NOT_FOUND)
        return CreditRequestResponse.model_validate(updated)

    @staticmethod
    def _build_access_query(current_user: dict) -> dict:
        tipo = str(current_user.get("tipo") or "").lower()
        usuario = current_user.get("idUsuario") or ""

        if tipo == "intermediario":
            return {"int_nit": usuario}
        if tipo == "cliente":
            return {"cli_cedula": usuario}
        return {}

    @staticmethod
    def _hydrate_actor_fields(data: dict, current_user: dict) -> None:
        tipo = str(current_user.get("tipo") or "").lower()
        usuario = current_user.get("idUsuario") or ""
        nombre = current_user.get("nombre")

        if tipo == "asesor":
            data.setdefault("ase_ced", usuario)
            if nombre:
                data.setdefault("ase_nom", nombre)
        elif tipo == "intermediario":
            data.setdefault("int_nit", usuario)
            if nombre:
                data.setdefault("int_nom", nombre)
        elif tipo == "cliente":
            data.setdefault("cli_cedula", usuario)
