from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CreditRequestBase(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    cli_cedula: str | None = None
    tipo_persona: str | None = None
    razon: str | None = None
    nom1: str | None = None
    nom2: str | None = None
    ape1: str | None = None
    ape2: str | None = None
    tipodoc: str | int | None = None
    email: str | None = None
    email_facturacion: str | None = None
    direccion: str | None = None
    ciudad: str | None = None
    telefono: str | int | None = None
    celular: str | int | None = None
    fecha_poliza: str | None = None
    fecha_poliza2: str | None = None
    cuotas: int | None = None
    poliza: int | float | None = None
    primeracuota: str | None = None
    cuotas_max: str | int | None = None
    min: int | float | None = None
    inicial: int | float | None = None
    interes_anual: int | float | None = None
    recursos: str | None = None
    numpoliza: str | None = None
    certifica: str | None = None
    seg_nombre: str | None = None
    seg_nit: int | str | None = None
    cod_ramo: str | None = None
    nom_ramo: str | None = None
    codseg: str | None = None
    int_nit: str | None = None
    int_nom: str | None = None
    int_cel: int | str | None = None
    int_tel: int | str | None = None
    int_email: str | None = None
    int_ciudad: str | None = None
    credito: str | None = None
    pagare: int | None = None
    placa: str | None = None
    estado: str | None = None
    ase_ced: str | None = None
    ase_nom: str | None = None
    ciuu: str | None = None
    regimen: int | str | None = None
    responsabilidad: list[str] | None = None
    archivos: list[str] | None = None
    estado_credito: str | None = None
    envio_pago: str | None = None
    envio_firma: str | None = None
    request_url: str | None = None
    cliente_valido: str | None = None
    metodo: str | None = None
    soli_diligenciada: str | None = None
    soli_firmada: str | None = None
    soli_documentos: str | None = None
    soli_pagada: str | None = None
    aut_conta: str | None = None
    plan_de_pagos: list[Any] | None = None
    cotizacion_valida: str | None = None
    fecha_de_pago: str | None = None
    dias_limite: int | None = None
    fecha_primera_cuota: str | None = None
    percent_ci: int | float | None = None


class CreditRequestCreate(CreditRequestBase):
    cli_cedula: str | None = None


class CreditRequestUpdate(CreditRequestBase):
    pass


class CreditRequestResponse(CreditRequestBase):
    id: str
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class CreditRequestListResponse(BaseModel):
    data: list[CreditRequestResponse]
    total: int


class CreditRequestDetailResponse(CreditRequestResponse):
    pass


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
