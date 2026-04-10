from fastapi import FastAPI

from app.api.router import api_router
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(
    title="Exxtra FastAPI",
    version="0.1.0",
    description="API migration for Exxtra built with FastAPI and MongoDB.",
)

register_exception_handlers(app)
app.include_router(api_router, prefix="/api")


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
