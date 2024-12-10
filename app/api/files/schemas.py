from __future__ import annotations
from typing_extensions import Literal

from pydantic import Field, BaseModel
from app.api.files.examples import (
    ex_file_create,
    ex_file_response,
    ex_file_remove
)


class Files(BaseModel):
    token: str
    user_id: int
    type_id: int


class FileCreate(BaseModel):
    token: str = Field(...)
    user_id: int = Field(...)
    type_id: int = Field(...)

    class Config:
        from_attributes = True
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_file_create
        }


class FileResponse(BaseModel):
    url: str
    file_path: str

    class Config:
        from_attributes = True
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_file_response
        }


class FileRemove(BaseModel):
    message: str

    class Config:
        from_attributes = True
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_file_remove
        }
