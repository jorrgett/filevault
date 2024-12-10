from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class IDModelMixin(BaseModel):
    id: int = Field(0, alias="id")


class CommonBase(IDModelMixin):
    class Config:
        from_attributes = True
        str_strip_whitespace = True


class DateMixin(BaseModel):
    created_at: datetime
    updated_at: Optional[datetime]
