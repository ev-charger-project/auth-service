from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.core.dependencies import get_current_super_user
from app.core.exceptions import AuthError
from app.core.security import JWTBearer
from app.schema.base_schema import Blank, FindResult
from app.schema.user_schema import CreateUser, FindUser, UpdateUser, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["user"], dependencies=[Depends(JWTBearer())])


@router.get("", response_model=FindResult[UserResponse])
@inject
async def get_user_list(
    find_query: FindUser = Depends(),
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: UserResponse = Depends(get_current_super_user),
):
    if not current_user.is_superuser:
        raise AuthError("Permission denied")

    return service.get_list(find_query)


@router.get("/{user_id}", response_model=UserResponse)
@inject
async def get_user(
    user_id: str,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: UserResponse = Depends(get_current_super_user),
):
    if not current_user.is_superuser:
        raise AuthError("Permission denied")
    return service.get_by_id(user_id)


@router.post("", response_model=UserResponse)
@inject
async def create_user(
    user: CreateUser,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: UserResponse = Depends(get_current_super_user),
):
    if not current_user.is_superuser:
        raise AuthError("Permission denied")
    return service.add(user)


@router.patch("/{user_id}", response_model=UserResponse)
@inject
async def update_user(
    user_id: str,
    user: UpdateUser,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: UserResponse = Depends(get_current_super_user),
):
    if not current_user.is_superuser:
        raise AuthError("Permission denied")
    return service.patch(user_id, user)


@router.delete("/{user_id}", response_model=Blank)
@inject
async def delete_user(
    user_id: str,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: UserResponse = Depends(get_current_super_user),
):
    if not current_user.is_superuser:
        raise AuthError("Permission denied")
    service.remove_by_id(user_id)
    return Blank()
