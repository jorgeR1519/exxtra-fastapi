from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class ClientBase(BaseModel):
    cli_cedula: str = Field(min_length=5, max_length=20)
    cli_nombre: str = Field(min_length=3, max_length=150)
    cli_email: EmailStr | None = None
    cli_telefono: str | None = Field(default=None, min_length=7, max_length=20)
    cli_cel: str | None = Field(default=None, min_length=7, max_length=20)
    cli_activo: bool = True
    fecha: str | None = None

    @field_validator("cli_cedula", "cli_telefono", "cli_cel")
    @classmethod
    def validate_numeric_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        clean_value = value.strip()
        if not clean_value.isdigit():
            raise ValueError("This field must contain only digits.")
        return clean_value

    @field_validator("cli_nombre")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.strip()


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    cli_nombre: str | None = Field(default=None, min_length=3, max_length=150)
    cli_email: EmailStr | None = None
    cli_telefono: str | None = Field(default=None, min_length=7, max_length=20)
    cli_cel: str | None = Field(default=None, min_length=7, max_length=20)
    cli_activo: bool | None = None
    fecha: str | None = None

    @field_validator("cli_telefono", "cli_cel")
    @classmethod
    def validate_numeric_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        clean_value = value.strip()
        if not clean_value.isdigit():
            raise ValueError("This field must contain only digits.")
        return clean_value

    @field_validator("cli_nombre")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return value.strip()


class ClientResponse(ClientBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class ClientListResponse(BaseModel):
    data: list[ClientResponse]
    total: int
