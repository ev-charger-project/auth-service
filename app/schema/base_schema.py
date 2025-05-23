import enum
from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field


class ModelBaseInfo(BaseModel):
    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ListOrderOptions(str, enum.Enum):
    desc = "desc"
    asc = "asc"


UPDATED_AT = "updated_at"


class PaginationQuery(BaseModel):
    ordering: Optional[ListOrderOptions] = ListOrderOptions.desc
    page: Optional[int] = Field(default=1, ge=1)
    page_size: Optional[int] = Field(default=10, ge=1)
    order_by: Optional[str] = UPDATED_AT

    @property
    def limit(self) -> int:
        return self.page_size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def desc(self) -> bool:
        if isinstance(self.order, str):
            return self.order == ListOrderOptions.desc.value
        return self.order == ListOrderOptions.desc


class SearchOptions(PaginationQuery):
    total_count: Optional[int]


T = TypeVar("T")


class FindResult(BaseModel, Generic[T]):
    founds: Optional[List[T]]
    search_options: Optional[SearchOptions]


class FindDateRange(BaseModel):
    created_at__lt: Optional[str] = None
    created_at__lte: Optional[str] = None
    created_at__gt: Optional[str] = None
    created_at__gte: Optional[str] = None


class Blank(BaseModel):
    pass
