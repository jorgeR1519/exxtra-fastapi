from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    idUsuario: str
    email: EmailStr
    tipo: str
    primeravez: str | None = None
    permisos: dict[str, bool] | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
