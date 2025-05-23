from datetime import datetime, timedelta

from app.core.config import configs
from app.core.exceptions import AuthError
from app.core.security import create_jwt_token, get_password_hash, verify_password
from app.model.refresh_token import RefreshToken
from app.model.user import User
from app.repository.refresh_token_repository import RefreshTokenRepository
from app.repository.user_repository import UserRepository
from app.schema.auth_schema import AuthResponse, SignIn, SignUp
from app.schema.base_schema import Blank
from app.services.base_service import BaseService


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository, refresh_token_repository: RefreshTokenRepository):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
        super().__init__(user_repository)

    def sign_in(self, sign_in_info: SignIn):
        user: User = self.user_repository.read_by_email(sign_in_info.email)
        if not user:
            raise AuthError(detail="Incorrect email or password")
        if not user.is_active:
            raise AuthError(detail="Account is not active")
        if not verify_password(sign_in_info.password, user.password):
            raise AuthError(detail="Incorrect email or password")
        refresh_token_lifespan = timedelta(days=configs.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token, expiration_datetime = create_jwt_token({"token_type": "refresh"}, refresh_token_lifespan)

        self.refresh_token_repository.create(
            RefreshToken(
                user_id=user.id,
                token=refresh_token,
                updated_at=datetime.now(),
                created_at=datetime.now(),
                expiration=datetime.now() + timedelta(days=configs.REFRESH_TOKEN_EXPIRE_DAYS),
                last_used=datetime.now(),
            )
        )

        access_token_lifespan = timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token, expiration_datetime = create_jwt_token({"subject": user.id.__str__(), "token_type": "access"}, access_token_lifespan)
        return AuthResponse(
            access_token=access_token,
            expiration=expiration_datetime,
            refresh_token=refresh_token,
        )

    def sign_out(self, refresh_token: str):
        self.refresh_token_repository.delete_session(refresh_token)
        return Blank()

    def refresh_token(self, refresh_token: str):
        new_token_lifespan = timedelta(days=configs.REFRESH_TOKEN_EXPIRE_DAYS)
        new_token, expiration_datetime = create_jwt_token({"token_type": "refresh"}, new_token_lifespan)
        current_token = self.refresh_token_repository.rotate_token(refresh_token, new_token)
        access_token, expiration_datetime = create_jwt_token({"subject": current_token.user_id.__str__(), "token_type": "access"})
        return AuthResponse(access_token=access_token, expiration=expiration_datetime, refresh_token=current_token.token)

    def sign_up(self, user_info: SignUp):
        user = User(
            **user_info.model_dump(exclude_none=True),
            is_active=True,
            is_superuser=False,
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )
        return self.user_repository.create(user)

    def get_me(self, user_id: str):
        return self.user_repository.read_by_id(user_id)
