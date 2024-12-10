from __future__ import annotations
from typing_extensions import Literal
from typing import Optional

from fastapi import HTTPException, status
from pydantic import Field, BaseModel, field_validator
from app.api.common import CommonBase, DateMixin
from app.api.types.examples import (
    ex_type_update,
    ex_type_create,
    ex_type_read,
)

allowed_format_files = ['jpeg', 'png', 'svg', 'gif', 'ico', 'pdf']
allowed_content_type = [
    'image/gif',
    'image/jpeg',
    'image/png',
    'image/svg+xml',
    'image/webp',
    'image/vnd.microsoft.icon',
    'application/pdf',
]
allowed_format_files = ['jpeg', 'png', 'svg', 'gif', 'ico', 'pdf']
allowed_content_type = [
    'image/gif',
    'image/jpeg',
    'image/png',
    'image/svg+xml',
    'image/webp',
    'image/vnd.microsoft.icon',
    'application/pdf',
]


class Types(BaseModel):
    app_id: int
    width: int
    height: int
    name: str
    size: int
    file_format: str
    content_type: str
    content_type: str

class TypeSchema(DateMixin, Types, CommonBase):
    class Config:
        from_attributes = True
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_type_read
        }


class TypeCreate(BaseModel):
    app_id: int = Field(...)
    width: int = Field(...)
    height: int = Field(...)
    name: str = Field(...)
    size: int = Field(...)
    file_format: str = Field(...)
    content_type: str = Field(...)
    content_type: str = Field(...)
    class Config:
        from_attributes = True
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_type_create
        }

    @field_validator("file_format")
    def validate_format(cls, v):
        if not v in allowed_format_files:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                    'message': f"The following types of formats are supported: {allowed_format_files}"})
        return v
    
    @field_validator("content_type")
    def validate_content_type(cls, v):
        if not v in allowed_content_type:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                    'message': f"The following types of formats are supported: {allowed_content_type}"})
        return v


class TypeUpdate(BaseModel):
    app_id: int = Field(...)
    width: Optional[int] = None
    height: Optional[int] = None
    name: Optional[str] = None
    size: Optional[int] = None
    file_format: Optional[str] = None
    content_type: Optional[str] = None
    content_type: Optional[str] = None
    class Config:
        from_attributes = True
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_type_update
        }
