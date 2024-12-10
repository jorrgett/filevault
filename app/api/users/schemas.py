from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel, EmailStr
from app.api.common import CommonBase, DateMixin
from app.api.users.examples import (
    ex_user_create,
    ex_user_update,
    ex_user_read,
)


class User(BaseModel):
    full_name: str
    email: str


class UserSchema(DateMixin, User, CommonBase):
    class Config:
        from_attributes = True
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_user_read
        }


class UserCreate(BaseModel):
    full_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    email: EmailStr = Field(
        ...
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=50
    )

    class Config:
        from_attributes = True
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_user_create
        }


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str = Field(
        ...,
        min_length=6,
        max_length=50
    )

    class Config:
        from_attributes = True
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_user_update
        }
