from typing import Callable

from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.helpers.jwt_handler import decodeJWT
from app.helpers.jwt_bearer import JWTBearer
from app.api.users.repository import UserRepository
from app.api.auth.repository import AuthRepository
from app.api.users.schemas import UserSchema
from app.resources.strings import NOT_PERMISSION


def _get_repository(repo: Callable) -> Callable:
    return repo


def _get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(JWTBearer()),
    user: UserRepository = Depends(
        _get_repository(UserRepository)
    )
):
    decode = decodeJWT(token)
    get_user = user.get_user_by_email(db, decode['email'])

    return UserSchema(__root__=get_user)


class PermissionChecker:

    def __init__(self, permission, user) -> None:
        self.permission = permission

    def __call__(self, data: UserSchema = Depends(_get_current_user)) -> bool:

        user = data.__root__.dict()

        for items in user['roles'][0]['permissions']:
            if self.permission == items['name']:
                return user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": 11,
                "message": NOT_PERMISSION
            }
        )


def get_auth_operations(
        session: Session = Depends(get_db)
) -> AuthRepository:
    return AuthRepository(session=session)
