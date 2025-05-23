from datetime import datetime

from pydantic import BaseModel

from app.schema.user_schema import UserResponse


class SignIn(BaseModel):
    email: str
    password: str


class SignUp(BaseModel):
    email: str
    password: str
    name: str
    phone_number: str


class Payload(BaseModel):
    id: str
    email: str
    name: str
    is_superuser: bool


class TokenPayload(BaseModel):
    subject: str
    exp: datetime
    token_type: str
    jti: str


class RefreshToken(BaseModel):
    refresh_token: str
    access_token: str


class AuthResponse(BaseModel):
    access_token: str
    expiration: datetime
    refresh_token: str


class SignInResponse(AuthResponse):
    user_info: UserResponse | None = None
