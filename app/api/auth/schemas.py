from __future__ import annotations

from pydantic import BaseModel, Field, EmailStr
from app.api.users.schemas import UserSchema
from app.api.auth.examples import (
    ex_authorization,
    ex_refresh_token,
    ex_user_login,
    ex_user_forget,
    ex_forget_response,
    ex_recovery_password,
    ex_generate_token
)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    ttl: int

    class Config:
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_authorization
        }


class refreshTokenSchema(BaseModel):
    token: str = Field(
        ...
    )

    class Config:
        json_schema_extra = {
            "example": ex_refresh_token
        }


class AuthorizationSchema(BaseModel):
    authorization: TokenSchema
    user: UserSchema


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(
        ...
    )
    password: str = Field(
        ...
    )

    class Config:
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_user_login
        }


class forgetPassword(BaseModel):
    email: EmailStr = Field(
        ...
    )

    class Config:
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_user_forget
        }


class forgetResponse(BaseModel):
    message: str

    class Config:
        json_schema_extra = {
            "example": ex_forget_response
        }


class recoveryPassword(BaseModel):
    code: str = Field(
        ...
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=16
    )

    class Config:
        str_strip_whitespace = True
        json_schema_extra = {
            "example": ex_recovery_password
        }


class PasswordCheck(BaseModel):
    password: str


class GenerateTokenSchema(BaseModel):
    token: str

    class Config:
        json_schema_extra = {
            "example": ex_refresh_token
        }


class CreateTokenSchema(BaseModel):
    code: str = Field(...)
    secret_key: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": ex_generate_token
        }
