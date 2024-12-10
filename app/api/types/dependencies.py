from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.types.repository import TypeRepository


def get_type_crud(
        session: Session = Depends(get_db)
) -> TypeRepository:
    return TypeRepository(session=session)
