from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.api.types.models import (
    Type
)


class TypeRepository():
    def __init__(self, session: Session):
        self.session = session
        self.now = datetime.utcnow()
        self.expire = timedelta(minutes=30)

    def get_all(
        self,
        app_id: int = None,
    ) -> Type:
        if app_id:
            query = self.session.execute(select(Type).where(Type.app_id == app_id))
        else:
            query = self.session.execute(select(Type))
            
        Types = query.scalars().all()

        return Types

    def get_by_id(
            self,
            type_id: int) -> Type:

        response = Type.find(self.session, type_id)

        return response

    def create(
        self,
        payload: Type
    ) -> Type:

        types = Type(**payload.dict(exclude_unset=True))

        types.save(self.session)
        return types

    def update(
        self,
        type_id: int,
        payload: Type
    ) -> Type:

        type = Type.find(self.session, type_id)
        type.update(self.session, **payload.dict(exclude_unset=True))

        return type

    def remove(
        self,
        type_id: int,
    ) -> None:

        type = Type.find(
            self.session,
            type_id,
        )

        type.delete(self.session)

        return type
