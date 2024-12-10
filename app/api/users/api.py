from typing import Annotated

from fastapi import APIRouter, Depends, Path, Body
from fastapi import status as http_status

from app.core.utils.paginate import Page, paginate
from app.api.users.repository import UserRepository as repository
from app.api.users.dependencies import get_user_crud
from app.helpers.jwt_bearer import JWTBearer
from app.api.users.schemas import (
    UserSchema,
    UserCreate,
    UserUpdate
)

router = APIRouter()


@router.get(
    "",
    response_model=Page[UserSchema],
    status_code=http_status.HTTP_200_OK,
    summary="Display a listing of the users",
    dependencies=[Depends(JWTBearer())]
)
def get_all_users(
    users: repository = Depends(get_user_crud)
) -> Page[UserSchema]:
    """Get all users associated with a company"""

    user = users.get_all()

    return paginate(user)


@router.get(
    "/{user_id}",
    response_model=UserSchema,
    status_code=http_status.HTTP_200_OK,
    summary="Get the specific user by ID",
    dependencies=[Depends(JWTBearer())]
)
def get_user_by_id(
    user_id: Annotated[int, Path(
        ...,
        title="User ID",
        description="This is User ID. Must be greater than 0",
        gt=0
    )],
    users: repository = Depends(get_user_crud)
) -> UserSchema:
    """Get first user associated with a company"""

    user = users.get_by_id(
        user_id=user_id
    )

    return user


@router.post(
    "",
    response_model=UserSchema,
    status_code=http_status.HTTP_201_CREATED,
    summary="Store a newly created user in storage",
    dependencies=[Depends(JWTBearer())]
)
def create_user(
    payload: UserCreate = Body(...),
    users: repository = Depends(get_user_crud)
) -> UserSchema:
    """Store a new user in storage"""

    user = users.create(
        payload=payload
    )

    return user


@router.put(
    "/{user_id}",
    response_model=UserSchema,
    status_code=http_status.HTTP_200_OK,
    summary="Update the specified user in storage",
    dependencies=[Depends(JWTBearer())]
)
def update_user_by_id(
    user_id: Annotated[int, Path(
        ...,
        title="User ID",
        description="This is User ID. Must be greater than 0",
        gt=0
    )],
    payload: UserUpdate = Body(...),
    users: repository = Depends(get_user_crud)
) -> UserSchema:
    """Update the specified user by ID"""

    user = users.update(
        user_id=user_id,
        payload=payload
    )

    return user


@router.delete(
    "/{user_id}",
    response_model=None,
    status_code=http_status.HTTP_204_NO_CONTENT,
    summary="Remove the specified user in storage",
    dependencies=[Depends(JWTBearer())]
)
def remove_app_by_id(
    user_id: Annotated[int, Path(
        ...,
        title="User ID",
        description="This is User ID. Must be greater than 0",
        gt=0
    )],
    users: repository = Depends(get_user_crud)
) -> None:
    """Remove the specified type by ID"""

    user = users.remove(user_id=user_id)

    return user
