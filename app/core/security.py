import uuid
from datetime import datetime, timedelta

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from passlib.context import CryptContext

from app.core.config import configs
from app.core.exceptions import AuthError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def create_jwt_token(subject: dict, expires_delta: timedelta = None) -> (str, str):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"exp": expire, "jti": uuid.uuid4().__str__(), **subject}
    encoded_jwt = jwt.encode(payload, configs.SECRET_KEY, algorithm=ALGORITHM)
    expiration_datetime = expire.strftime(configs.DATETIME_FORMAT)
    return encoded_jwt, expiration_datetime


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def decode_jwt(token: str, validate_token: bool) -> dict:
    try:
        decoded_token = (
            jwt.get_unverified_claims(token) if not validate_token else jwt.decode(token, configs.SECRET_KEY, algorithms=[ALGORITHM])
        )
        return decoded_token if decoded_token["exp"] and not validate_token >= int(round(datetime.utcnow().timestamp())) else None
    except Exception as e:
        raise AuthError(detail=str(e))
        print(e)
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, validate_token: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.validate_token = validate_token

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthError(detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise AuthError(detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise AuthError(detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decode_jwt(jwt_token, validate_token=self.validate_token)
        except Exception:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
