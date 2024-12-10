from typing import Annotated

from fastapi import APIRouter, Depends, Path, Body
from fastapi import status as http_status

from app.core.utils.paginate import Page, paginate
from app.api.applications.repository import ApplicationRepository as repository
from app.api.applications.dependencies import get_app_crud
from app.helpers.jwt_bearer import JWTBearer
from app.api.applications.schemas import (
    AppSchema,
    AppCreate,
    AppUpdate
)

router = APIRouter()


@router.get(
    "",
    response_model=Page[AppSchema],
    status_code=http_status.HTTP_200_OK,
    summary="Display a listing of the apps",
    dependencies=[Depends(JWTBearer())]
)
def get_all_apps(
    apps: repository = Depends(get_app_crud)
) -> Page[AppSchema]:
    """Get all apps associated with a company"""

    app = apps.get_all()

    return paginate(app)


@router.get(
    "/{app_id}",
    response_model=AppSchema,
    status_code=http_status.HTTP_200_OK,
    summary="Get the specific app by ID",
    dependencies=[Depends(JWTBearer())]
)
def get_app_by_id(
    app_id: Annotated[int, Path(
        ...,
        title="App ID",
        description="This is App ID. Must be greater than 0",
        gt=0
    )],
    apps: repository = Depends(get_app_crud)
) -> AppSchema:
    """Get first app associated with a company"""

    app = apps.get_by_id(
        app_id=app_id
    )

    return app


@router.post(
    "",
    response_model=AppSchema,
    status_code=http_status.HTTP_201_CREATED,
    summary="Store a newly created app in storage",
    dependencies=[Depends(JWTBearer())]
)
def create_app(
    payload: AppCreate = Body(...),
    apps: repository = Depends(get_app_crud)
):  # -> AppSchema:
    """Store a new app in storage"""

    app = apps.create(
        payload=payload
    )

    return app


@router.put(
    "/{app_id}",
    response_model=AppSchema,
    status_code=http_status.HTTP_200_OK,
    summary="Update the specified app in storage",
    dependencies=[Depends(JWTBearer())]
)
def update_app_by_id(
    app_id: Annotated[int, Path(
        ...,
        title="App ID",
        description="This is App ID. Must be greater than 0",
        gt=0
    )],
    payload: AppUpdate = Body(...),
    apps: repository = Depends(get_app_crud)
) -> AppSchema:
    """Update the specified app by ID"""

    app = apps.update(
        app_id=app_id,
        payload=payload
    )

    return app


@router.delete(
    "/{app_id}",
    response_model=None,
    status_code=http_status.HTTP_204_NO_CONTENT,
    summary="Remove the specified app in storage",
    dependencies=[Depends(JWTBearer())]
)
def remove_app_by_id(
    app_id: Annotated[int, Path(
        ...,
        title="App ID",
        description="This is App ID. Must be greater than 0",
        gt=0
    )],
    apps: repository = Depends(get_app_crud)
) -> None:
    """Remove the specified app by ID"""

    app = apps.remove(app_id=app_id)

    return app
