from fastapi import (
    APIRouter, Depends, Body,
    HTTPException, status
)

from app.api.auth.repository import AuthRepository
from app.api.users.repository import UserRepository
from app.helpers.jwt_bearer import JWTBearer

from app.api.auth.dependencies import get_auth_operations
from app.api.users.dependencies import get_user_crud
from app.api.auth.schemas import (
    UserLoginSchema,
    AuthorizationSchema,
    forgetPassword,
    forgetResponse,
    recoveryPassword,
    refreshTokenSchema,
    GenerateTokenSchema,
    CreateTokenSchema
)

router = APIRouter()


@router.post(
    "/login",
    response_model=AuthorizationSchema,
    status_code=status.HTTP_200_OK,
    summary="Set connection with API",
    name="auth:login"
)
def start_session(
        payload: UserLoginSchema = Body(...),
        auth: AuthRepository = Depends(get_auth_operations),
        user: UserRepository = Depends(get_user_crud)
):
    """Set login with the service"""

    result = auth.login(payload=payload, user=user)
    return result


@router.post(
    path='/forget-password',
    summary="Forget Password",
    response_model=forgetResponse,
    status_code=status.HTTP_200_OK,
    name="auth:forget"
)
def account_forget(
    payload: forgetPassword = Body(...),
    auth: AuthRepository = Depends(get_auth_operations),
    user: UserRepository = Depends(get_user_crud)
) -> forgetResponse:
    """Forget Password"""

    send_email = auth.forget_password(payload=payload, user=user)

    if not send_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Whoops, code could not be sent, contact support"
        )

    return {
        'message': 'The email has been sent to reset your password'
    }


@router.post(
    path='/reset-password',
    summary="Reset Password",
    response_model=AuthorizationSchema,
    status_code=status.HTTP_200_OK,
    name="auth:reset"
)
def account_reset(
    payload: recoveryPassword = Body(...),
    auth: AuthRepository = Depends(get_auth_operations),
    user: UserRepository = Depends(get_user_crud)
) -> AuthorizationSchema:
    """Reset Password"""

    result = auth.reset_password(payload=payload, user=user)
    return result


@router.post(
    path='/refresh',
    summary="Refresh Token",
    response_model=AuthorizationSchema,
    status_code=status.HTTP_200_OK,
    name="auth:refresh"
)
def account_refresh(
    payload: refreshTokenSchema = Body(...),
    auth: AuthRepository = Depends(get_auth_operations),
    user: UserRepository = Depends(get_user_crud)
) -> AuthorizationSchema:
    """Refresh Token"""

    result = auth.refresh(payload=payload, user=user)
    return result


@router.post(
    path='/generate_token',
    summary="Generate the service token",
    response_model=GenerateTokenSchema,
    status_code=status.HTTP_200_OK,
    name="auth:token",
)
def service_token(
    payload: CreateTokenSchema = Body(...),
    auth: AuthRepository = Depends(get_auth_operations),
) -> AuthorizationSchema:
    """Generate the token that will be used to communicate with the S3 endpoints."""

    result = auth.generate_token(payload=payload)
    return result
