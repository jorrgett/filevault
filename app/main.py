from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.errors.http_error import http_error_handler
from app.core.errors.validation_error import http422_error_handler
from app.router.endpoints import api_router
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check


def get_application() -> FastAPI:

    settings = get_settings()
    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(
        RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix='/api')

    disable_installed_extensions_check()
    add_pagination(application)

    return application


app = get_application()
