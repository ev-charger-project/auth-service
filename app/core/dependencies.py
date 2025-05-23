from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from jose import jwt
from pydantic import ValidationError

from app.core.config import configs
from app.core.container import Container
from app.core.exceptions import AuthError
from app.core.security import ALGORITHM, JWTBearer
from app.model.user import User
from app.schema.auth_schema import TokenPayload
from app.services.user_service import UserService


@inject
def get_current_user(
    token: str = Depends(JWTBearer()),
    service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=ALGORITHM)
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise AuthError(detail="Could not validate credentials")
    current_user: User = service.get_by_id(token_data.subject)
    if not current_user:
        raise AuthError(detail="User not found")
    return current_user


@inject
def validate_token(
    token: str = Depends(JWTBearer()),
) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=ALGORITHM)
        if payload["token_type"] != "access":
            raise AuthError(detail="Invalid token type")
        return payload
    except (jwt.JWTError, ValidationError):
        raise AuthError(detail=ValidationError.json())


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    return current_user


def get_current_user_with_no_exception(
    token: str = Depends(JWTBearer(validate_token=False)),
    service: UserService = Depends(Provide[Container.user_service]),
) -> dict[str, Any] | None:
    try:
        return jwt.get_unverified_claims(token)
    except (jwt.JWTError, ValidationError):
        return None


def get_current_super_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    if not current_user.is_superuser:
        raise AuthError("It's not a super user")
    return current_user
