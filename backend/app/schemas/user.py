from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    idUsuario: str
    email: EmailStr
    tipo: str
    nombre: str | None = None
    primeravez: str | None = None
    permisos: dict[str, bool] | None = None
    activo: bool | None = None
    verificado: bool | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class UserCreateRequest(BaseModel):
    id_usuario: str = Field(min_length=3, max_length=50, alias="idUsuario")
    email: EmailStr
    contrasena: str = Field(min_length=6, max_length=128)
    tipo: str = Field(min_length=6, max_length=20)
    nombre: str | None = Field(default=None, min_length=3, max_length=120)
    primeravez: str = Field(default="si", min_length=2, max_length=5)
    permisos: dict[str, bool] | None = None
    activo: bool = True
    verificado: bool = True

    model_config = {"populate_by_name": True}

    @field_validator("id_usuario", "tipo", "primeravez")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("nombre")
    @classmethod
    def normalize_optional_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return value.strip()


class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
    contrasena: str | None = Field(default=None, min_length=6, max_length=128)
    tipo: str | None = Field(default=None, min_length=6, max_length=20)
    nombre: str | None = Field(default=None, min_length=3, max_length=120)
    primeravez: str | None = Field(default=None, min_length=2, max_length=5)
    permisos: dict[str, bool] | None = None
    activo: bool | None = None
    verificado: bool | None = None

    @field_validator("tipo", "primeravez")
    @classmethod
    def normalize_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return value.strip()

    @field_validator("nombre")
    @classmethod
    def normalize_optional_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return value.strip()


class UserListResponse(BaseModel):
    data: list[UserResponse]
    total: int
