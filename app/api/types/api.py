from typing import Annotated

from fastapi import APIRouter, Depends, Path, Body
from fastapi import status as http_status

from app.core.utils.paginate import Page, paginate
from app.api.types.repository import TypeRepository as repository
from app.api.types.dependencies import get_type_crud
from app.helpers.jwt_bearer import JWTBearer
from app.api.types.schemas import (
    TypeSchema,
    TypeCreate,
    TypeUpdate
)

router = APIRouter()


@router.get(
    "",
    response_model=Page[TypeSchema],
    status_code=http_status.HTTP_200_OK,
    summary="Display a listing of the types",
    dependencies=[Depends(JWTBearer())]
)
def get_all_types(
    app_id: int = None,
    types: repository = Depends(get_type_crud)
) -> Page[TypeSchema]:
    """Get all types associated with a company"""

    type = types.get_all(app_id=app_id)

    return paginate(type)


@router.get(
    "/{type_id}",
    response_model=TypeSchema,
    status_code=http_status.HTTP_200_OK,
    summary="Get the specific type by ID",
    dependencies=[Depends(JWTBearer())]
)
def get_type_by_id(
    type_id: Annotated[int, Path(
        ...,
        title="Type ID",
        description="This is Type ID. Must be greater than 0",
        gt=0
    )],
    types: repository = Depends(get_type_crud)
) -> TypeSchema:
    """Get first type associated with a company"""

    type = types.get_by_id(
        type_id=type_id
    )

    return type


@router.post(
    "",
    response_model=TypeSchema,
    status_code=http_status.HTTP_201_CREATED,
    summary="Store a newly created type in storage",
    dependencies=[Depends(JWTBearer())]
)
def create_type(
    payload: TypeCreate = Body(...),
    types: repository = Depends(get_type_crud)
) -> TypeSchema:
    """Store a new type in storage"""

    type = types.create(
        payload=payload
    )

    return type


@router.put(
    "/{type_id}",
    response_model=TypeSchema,
    status_code=http_status.HTTP_200_OK,
    summary="Update the specified type in storage",
    dependencies=[Depends(JWTBearer())]
)
def update_type_by_id(
    type_id: Annotated[int, Path(
        ...,
        title="Type ID",
        description="This is Type ID. Must be greater than 0",
        gt=0
    )],
    payload: TypeUpdate = Body(...),
    types: repository = Depends(get_type_crud)
) -> TypeSchema:
    """Update the specified type by ID"""

    type = types.update(
        type_id=type_id,
        payload=payload
    )

    return type


@router.delete(
    "/{type_id}",
    response_model=None,
    status_code=http_status.HTTP_204_NO_CONTENT,
    summary="Remove the specified type in storage",
    dependencies=[Depends(JWTBearer())]
)
def remove_app_by_id(
    type_id: Annotated[int, Path(
        ...,
        title="Type ID",
        description="This is Type ID. Must be greater than 0",
        gt=0
    )],
    types: repository = Depends(get_type_crud)
) -> None:
    """Remove the specified type by ID"""

    type = types.remove(type_id=type_id)

    return type
