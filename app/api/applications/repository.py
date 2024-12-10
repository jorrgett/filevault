from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.helpers.jwt_handler import get_password_hash
from app.api.applications.models import Application


class ApplicationRepository():
    def __init__(self, session: Session):
        self.session = session
        self.now = datetime.utcnow()
        self.expire = timedelta(minutes=30)

    def get_all(
        self,
    ) -> Application:

        query = self.session.execute(select(Application))
        Applications = query.scalars().all()

        return Applications

    def get_by_id(
            self,
            app_id: int) -> Application:

        response = Application.find(self.session, app_id)

        return response

    def create(
        self,
        payload: Application
    ) -> Application:

        payload.secret = get_password_hash(payload.secret)
        app = Application(**payload.dict(exclude_unset=True))

        app.save(self.session)

        return app

    def update(
        self,
        app_id: int,
        payload: Application
    ) -> Application:

        application = Application.find(self.session, app_id)

        if payload.secret:
            payload.secret = get_password_hash(payload.secret)

        application.update(self.session, **payload.dict(exclude_unset=True))

        return application

    def remove(
        self,
        app_id: int,
    ) -> None:

        application = Application.find(
            self.session,
            app_id,
        )

        application.delete(self.session)

        return application
