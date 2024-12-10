import random
import string
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.helpers.jwt_handler import get_password_hash
from app.api.users.models import (
    User, UserRecovery
)


class UserRepository():
    def __init__(self, session: Session):
        self.session = session
        self.now = datetime.utcnow()
        self.expire = timedelta(minutes=30)

    def get_all(
        self,
    ) -> User:

        return self.session.query(User).all()

    def get_by_id(
            self,
            user_id: int) -> User:

        query = self.session.execute(
            select(User).where(
                (User.id == user_id)
            )
        )
        user = query.scalars().first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": 1,
                    "message": f"There is no record for requested user value: {user_id}"},
            )
        else:
            return user

    def get_by_email(
            self,
            email: str) -> User:

        query = self.session.execute(
            select(User).where(
                (User.email == email)
            )
        )
        user = query.scalars().first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": 2,
                    "message": f"No user with this email: {email} has been found"},
            )
        else:
            return user

    def create(
        self,
        payload: User
    ) -> User:

        payload.password = get_password_hash(payload.password)
        user = User(**payload.model_dump())

        user.save(self.session)

        return self.get_by_id(user_id=user.id)

    def update(
        self,
        user_id: int,
        payload: User
    ) -> User:

        user = User.find(
            self.session,
            user_id,
        )

        payload.password = get_password_hash(payload.password)
        user.update(self.session, **payload.dict(exclude_unset=True))

        return user

    def set_token_to_recovery(self, user_id):

        set_token = UserRecovery(**{
            'user_id': user_id,
            'code': self.get_random_string(6),
            'expire_date': (self.now + self.expire)
        })

        set_token.save(self.session)
        return set_token

    def get_random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def check_user_request_recovery(self, code):
        query = self.session.execute(
            select(UserRecovery).options(
                selectinload(UserRecovery.user)).where(
                    (UserRecovery.code == code)
            ))

        recovery = query.scalars().first()

        if recovery and (
            recovery.expire_date >= (self.now)
        ):
            return recovery.user

        return False

    def remove(
        self,
        user_id: int,
    ) -> None:

        user = User.find(
            self.session,
            user_id,
        )

        user.delete(self.session)

        return user
