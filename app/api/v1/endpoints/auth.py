from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.core.dependencies import get_current_user_with_no_exception
from app.schema.auth_schema import AuthResponse, Payload, SignIn, SignUp
from app.schema.user_schema import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-in", response_model=AuthResponse)
@inject
async def sign_in(user_info: SignIn, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.sign_in(user_info)


@router.post("/sign-up", response_model=UserResponse)
@inject
async def sign_up(user_info: SignUp, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.sign_up(user_info)


@router.delete("/sign-out", response_model=None)
@inject
async def sign_out(token: str, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.sign_out(token)


@router.get("/refresh-token", response_model=AuthResponse)
@inject
async def refresh_token(token: str, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.refresh_token(token)


@router.get("/me", response_model=UserResponse | None)
@inject
async def get_me(
    me: Payload = Depends(get_current_user_with_no_exception), service: AuthService = Depends(Provide[Container.auth_service])
):
    return service.get_me(me["subject"])
