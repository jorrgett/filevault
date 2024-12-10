from __future__ import annotations
from typing import Optional, AnyStr

from pydantic import Field, BaseModel, validator
from app.api.common import CommonBase, DateMixin
from app.api.applications.examples import (
    ex_app_update,
    ex_app_create,
    ex_app_read,
)


class App(BaseModel):
    code: str
    name: str
    secret: str
    bucket_name: str
    bucket_key_id: str
    bucket_secret_key: str
    bucket_region: str
    bucket_invalidation_code: str
    cloudfront_url: str


class AppSchema(DateMixin, App, CommonBase):
    class Config:
        from_attributes = True
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_app_read
        }


class AppCreate(BaseModel):
    code: str = Field(...)
    secret: str = Field(...)
    name: str = Field(...)
    bucket_name: str = Field(...)
    bucket_key_id: str = Field(...)
    bucket_secret_key: str = Field(...)
    bucket_region: str = Field(...)
    cloudfront_url: str = Field(...)

    class Config:
        from_attributes = True
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_app_create
        }


class AppUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    secret: Optional[str] = None
    bucket_name: Optional[str] = None
    bucket_key_id: Optional[str] = None
    bucket_secret_key: Optional[str] = None
    bucket_region: Optional[str] = None
    cloudfront_url: Optional[str] = None

    class Config:
        from_attributes = True
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_app_update
        }
