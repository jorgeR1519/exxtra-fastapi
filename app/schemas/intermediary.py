from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.user import UserResponse


class IntermediaryBase(BaseModel):
    int_nit: str = Field(min_length=5, max_length=20)
    int_nombre: str = Field(min_length=3, max_length=150)
    int_email: EmailStr | None = None
    int_ciudad: str | None = Field(default=None, min_length=5, max_length=10)
    int_cel: str | None = Field(default=None, min_length=7, max_length=20)
    int_tel: str | None = Field(default=None, min_length=7, max_length=20)
    fecha: str | None = None

    @field_validator("int_nit", "int_ciudad", "int_cel", "int_tel")
    @classmethod
    def validate_numeric_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        clean_value = value.strip()
        if not clean_value.isdigit():
            raise ValueError("This field must contain only digits.")
        return clean_value

    @field_validator("int_nombre")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.strip()


class IntermediaryCreate(IntermediaryBase):
    pass


class IntermediaryUpdate(BaseModel):
    int_nombre: str | None = Field(default=None, min_length=3, max_length=150)
    int_email: EmailStr | None = None
    int_ciudad: str | None = Field(default=None, min_length=5, max_length=10)
    int_cel: str | None = Field(default=None, min_length=7, max_length=20)
    int_tel: str | None = Field(default=None, min_length=7, max_length=20)
    fecha: str | None = None

    @field_validator("int_ciudad", "int_cel", "int_tel")
    @classmethod
    def validate_numeric_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        clean_value = value.strip()
        if not clean_value.isdigit():
            raise ValueError("This field must contain only digits.")
        return clean_value

    @field_validator("int_nombre")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return value.strip()


class IntermediaryResponse(IntermediaryBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class IntermediaryListResponse(BaseModel):
    data: list[IntermediaryResponse]
    total: int


class IntermediaryRelationsResponse(BaseModel):
    intermediary: IntermediaryResponse
    linked_users: list[UserResponse]
    related_new_business_count: int
