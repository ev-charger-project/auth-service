from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicatedError
from app.core.security import get_password_hash
from app.model.user import User
from app.repository.base_repository import BaseRepository
from app.schema.user_schema import CreateUser


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, User)

    def read_by_email(self, email: str):
        with self.session_factory() as session:
            return session.query(User).filter(User.email.__eq__(email)).first()

    def delete_by_id(self, id: str):
        self.soft_delete_by_id(id)

    def create(self, schema: CreateUser):
        with self.session_factory() as session:
            schema.password = get_password_hash(schema.password)
            query = self.model(**schema.model_dump())
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
            except IntegrityError as e:
                raise DuplicatedError(detail=str(e.orig))
            return query
