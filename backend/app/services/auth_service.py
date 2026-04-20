from fastapi import status

from app.core.exceptions import AppException
from app.core.security import create_access_token, verify_password
from app.models.user import build_user_document
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse


class AuthService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()

    def register(self, payload: RegisterRequest) -> TokenResponse:
        existing_user = self.user_repository.get_by_email(payload.email, payload.tipo)
        if existing_user:
            raise AppException(
                detail="A user with this email and tipo already exists.",
                status_code=status.HTTP_409_CONFLICT,
            )

        user = self.user_repository.create(
            build_user_document(
                id_usuario=payload.id_usuario,
                email=payload.email,
                contrasena=payload.contrasena,
                tipo=payload.tipo,
                primeravez=payload.primeravez,
                permisos=payload.permisos,
            )
        )

        token = create_access_token(
            subject=user["id"],
            usuario=user["idUsuario"],
            tipo=user["tipo"],
            email=user.get("email"),
        )
        return TokenResponse(access_token=token, user=UserResponse.model_validate(user))

    def login(self, payload: LoginRequest) -> TokenResponse:
        user = self.user_repository.get_by_usuario(payload.usuario, include_password=True)
        if not user and "@" in payload.usuario:
            user = self.user_repository.get_by_email(payload.usuario, include_password=True)

        if not user or "contrasena" not in user or not verify_password(payload.contrasena, user["contrasena"]):
            raise AppException(
                detail="Usuario/Contrasena Incorrectos.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        token = create_access_token(
            subject=user["id"],
            usuario=user["idUsuario"],
            tipo=user["tipo"],
            email=user.get("email"),
        )
        return TokenResponse(access_token=token, user=UserResponse.model_validate(user))
