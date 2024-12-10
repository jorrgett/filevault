from typing import Annotated

from fastapi import (
    APIRouter, Depends,
    UploadFile, Form,
    File, Request
)
from fastapi import HTTPException, status as http_status

from app.api.files.repository import FileRepository as repository
from app.api.files.dependencies import get_file_repository
from app.helpers.jwt_handler import decodeJWT
from app.api.files.schemas import (
    Files,
    FileCreate,
    FileResponse,
    FileRemove
)

router = APIRouter()


@router.post(
    "/upload",
    response_model=FileResponse,
    status_code=http_status.HTTP_200_OK,
    summary="Update the specified type in storage"
)
def create_file(
    request: Request,
    file: Annotated[UploadFile, File()],
    token: Annotated[str, Form(
        title="Token",
        description="This is the token previously generated and customized to validate the application"
    )],
    type_id: Annotated[int, Form(
        title="Type ID",
        description="This is Type ID. Must be greater 0",
        gt=0
    )],
    user_id: Annotated[int, Form(
        title="User ID",
        description="This is User ID. Must be greater 0",
        gt=0
    )],
    files: repository = Depends(get_file_repository)
):
    security = decodeJWT(token, True)

    if not security:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED, detail={
                'message': "The token is expired or invalid"})

    return files.upload_file(
        file,
        token=token,
        type_id=type_id,
        user_id=user_id,
        app_id=security['app_id'],
        ip=request.client.host
    )


@router.post(
    "/remove",
    response_model=FileRemove,
    status_code=http_status.HTTP_200_OK,
    summary="Remove item from s3 storage"
)
def remove_file(
    request: Request,
    token: Annotated[str, Form(
        title="Token",
        description="This is the token previously generated and customized to validate the application"
    )],
    file_path: Annotated[str, Form(
        title="Path File",
        description="This is the relative path to the address of the folder where the image you uploaded above is located"
    )],
    user_id: Annotated[int, Form(
        title="User ID",
        description="This is User ID. Must be greater 0",
        gt=0
    )],
    files: repository = Depends(get_file_repository)
):
    security = decodeJWT(token, True)

    if not security:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED, detail={
                'message': "The token is expired or invalid"})

    return files.remove_file(
        file_path=file_path,
        app_id=security['app_id'],
        user_id=user_id,
        ip=request.client.host
    )
