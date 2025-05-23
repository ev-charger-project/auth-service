import datetime
import uuid

from sqlmodel import Field, SQLModel


class EntityVersionTracking:
    version: int = Field(default=1, nullable=False)


class OperationTimeTracking:
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    updated_at: datetime.datetime | None = Field(default=None, nullable=True)
    deleted_at: datetime.datetime | None = Field(default=None, nullable=True)


class OperationByTracking:
    created_by: uuid.UUID | None = Field(default=None, nullable=True)
    updated_by: uuid.UUID | None = Field(default=None, nullable=True)
    deleted_by: uuid.UUID | None = Field(default=None, nullable=True)


class BaseModel(SQLModel, OperationTimeTracking, OperationByTracking, EntityVersionTracking):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4, nullable=False, index=True)
    is_deleted: bool = Field(default=False, nullable=False)
