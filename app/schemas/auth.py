from pydantic import BaseModel, EmailStr, Field

from app.schemas.user import UserResponse


class RegisterRequest(BaseModel):
    id_usuario: str = Field(min_length=3, max_length=50, alias="idUsuario")
    email: EmailStr
    contrasena: str = Field(min_length=6, max_length=128)
    tipo: str = Field(min_length=6, max_length=20)
    primeravez: str = Field(default="si", min_length=2, max_length=5)
    permisos: dict[str, bool] | None = None

    model_config = {"populate_by_name": True}


class LoginRequest(BaseModel):
    usuario: str = Field(min_length=3, max_length=50)
    contrasena: str = Field(min_length=6, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
