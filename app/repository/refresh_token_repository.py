from contextlib import AbstractContextManager
from datetime import datetime, timedelta
from typing import Callable, Type

from sqlalchemy.orm import Session

from app.core.config import configs
from app.model.refresh_token import RefreshToken
from app.repository.base_repository import BaseRepository


class RefreshTokenRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, RefreshToken)

    def create(self, schema):
        with self.session_factory() as session:
            query = self.model(**schema.model_dump())
            session.add(query)
            session.commit()
            session.refresh(query)
            return query

    def delete_by_user_id(self, user_id):
        with self.session_factory() as session:
            session.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
            session.commit()
            return None

    def delete_session(self, token):
        with self.session_factory() as session:
            ss = session.query(RefreshToken).filter(RefreshToken.token == token).delete()
            session.commit()
            if not ss:
                raise ValueError("Token not found")
            return None

    def rotate_token(self, token, new_token) -> Type[RefreshToken]:
        with self.session_factory() as session:
            current_token = session.query(RefreshToken).filter(RefreshToken.token == token).first()
            if not current_token:
                raise Exception("Token not found")

            if current_token.expiration < datetime.now():
                raise Exception("Token is expired")

            current_token.token = new_token
            current_token.last_used = datetime.now()
            current_token.expiration = datetime.now() + timedelta(days=configs.REFRESH_TOKEN_EXPIRE_DAYS)
            session.commit()
            session.refresh(current_token)
            return current_token
