from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_current_admin
from app.schemas.user import UserCreateRequest, UserListResponse, UserResponse, UserUpdateRequest
from app.services.user_service import UserService

router = APIRouter()


@router.get("/usuarios", response_model=UserListResponse)
def list_users(
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=200),
    _: dict = Depends(get_current_admin),
) -> UserListResponse:
    return UserService().list_users(search=search, page=page, limit=limit)


@router.get("/usuario/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    _: dict = Depends(get_current_admin),
) -> UserResponse:
    return UserService().get_user(user_id)


@router.post("/usuario", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreateRequest,
    _: dict = Depends(get_current_admin),
) -> UserResponse:
    return UserService().create_user(payload)


@router.put("/usuario/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    payload: UserUpdateRequest,
    _: dict = Depends(get_current_admin),
) -> UserResponse:
    return UserService().update_user(user_id, payload)


@router.delete("/usuario/{user_id}")
def delete_user(
    user_id: str,
    current_admin: dict = Depends(get_current_admin),
) -> dict[str, str]:
    return UserService().delete_user(user_id, current_admin["id"])
