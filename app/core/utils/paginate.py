from fastapi import Query
from pydantic import Field
from fastapi_pagination.links import Page
from fastapi_pagination import paginate, pagination_ctx

Page = Page.with_custom_options(size=Query(10, ge=1, le=50))
