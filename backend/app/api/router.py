from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.catalog import router as catalog_router
from app.api.v1.clients import router as clients_router
from app.api.v1.credit_requests import router as credit_requests_router
from app.api.v1.intermediaries import router as intermediaries_router
from app.api.v1.users import router as users_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/v1/auth", tags=["auth"])
api_router.include_router(catalog_router, prefix="/v1", tags=["catalog"])
api_router.include_router(clients_router, prefix="/v1", tags=["clients"])
api_router.include_router(credit_requests_router, prefix="/v1", tags=["credit-requests"])
api_router.include_router(intermediaries_router, prefix="/v1", tags=["intermediaries"])
api_router.include_router(users_router, prefix="/v1", tags=["users"])
