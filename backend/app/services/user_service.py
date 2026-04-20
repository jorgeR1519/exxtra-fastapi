from fastapi import status

from app.core.exceptions import AppException
from app.core.security import hash_password
from app.models.user import build_user_document
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreateRequest, UserListResponse, UserResponse, UserUpdateRequest


class UserService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()

    def list_users(self, *, search: str | None = None, page: int = 1, limit: int = 50) -> UserListResponse:
        skip = (page - 1) * limit
        users, total = self.user_repository.list(search=search, skip=skip, limit=limit)
        return UserListResponse(data=[UserResponse.model_validate(user) for user in users], total=total)

    def get_user(self, user_id: str) -> UserResponse:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise AppException("Usuario no encontrado.", status.HTTP_404_NOT_FOUND)
        return UserResponse.model_validate(user)

    def create_user(self, payload: UserCreateRequest) -> UserResponse:
        existing_email = self.user_repository.get_by_email(payload.email, payload.tipo)
        if existing_email:
            raise AppException("Ya existe un usuario con este email y tipo.", status.HTTP_409_CONFLICT)

        existing_user = self.user_repository.get_by_usuario(payload.id_usuario)
        if existing_user:
            raise AppException("Ya existe un usuario con ese idUsuario.", status.HTTP_409_CONFLICT)

        user = self.user_repository.create(
            build_user_document(
                id_usuario=payload.id_usuario,
                email=payload.email,
                contrasena=payload.contrasena,
                tipo=payload.tipo,
                nombre=payload.nombre,
                primeravez=payload.primeravez,
                permisos=payload.permisos,
                activo=payload.activo,
                verificado=payload.verificado,
            )
        )
        return UserResponse.model_validate(user)

    def update_user(self, user_id: str, payload: UserUpdateRequest) -> UserResponse:
        current_user = self.user_repository.get_by_id(user_id)
        if not current_user:
            raise AppException("Usuario no encontrado.", status.HTTP_404_NOT_FOUND)

        update_data = payload.model_dump(exclude_none=True)

        if "email" in update_data or "tipo" in update_data:
            email = update_data.get("email", current_user["email"])
            tipo = update_data.get("tipo", current_user["tipo"])
            existing_email = self.user_repository.get_by_email(email, tipo)
            if existing_email and existing_email["id"] != user_id:
                raise AppException("Ya existe un usuario con este email y tipo.", status.HTTP_409_CONFLICT)

        if "contrasena" in update_data:
            update_data["contrasena"] = hash_password(update_data["contrasena"])

        updated_user = self.user_repository.update(user_id, update_data)
        if not updated_user:
            raise AppException("No fue posible actualizar el usuario.", status.HTTP_400_BAD_REQUEST)
        return UserResponse.model_validate(updated_user)

    def delete_user(self, user_id: str, current_user_id: str) -> dict[str, str]:
        if user_id == current_user_id:
            raise AppException("No puedes eliminar tu propio usuario.", status.HTTP_400_BAD_REQUEST)

        deleted = self.user_repository.delete(user_id)
        if not deleted:
            raise AppException("Usuario no encontrado.", status.HTTP_404_NOT_FOUND)
        return {"message": "Usuario eliminado correctamente."}
