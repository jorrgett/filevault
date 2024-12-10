from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.files.repository import FileRepository


def get_file_repository(
        session: Session = Depends(get_db)
) -> FileRepository:
    return FileRepository(session=session)
