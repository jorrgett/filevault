from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.applications.repository import ApplicationRepository


def get_app_crud(
        session: Session = Depends(get_db)
) -> ApplicationRepository:
    return ApplicationRepository(session=session)
