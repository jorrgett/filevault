from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.users.repository import UserRepository


def get_user_crud(
        session: Session = Depends(get_db)
) -> UserRepository:
    return UserRepository(session=session)
