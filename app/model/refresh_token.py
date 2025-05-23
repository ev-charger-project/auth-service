import uuid
from datetime import datetime

from sqlmodel import Field

from app.model import BaseModel


class RefreshToken(BaseModel, table=True):
    token: str = Field(unique=True, nullable=False)
    user_id: uuid.UUID = Field(nullable=False)
    expiration: datetime = Field(nullable=False)
    last_used: datetime = Field(nullable=False)
