from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import (
    Boolean, Column, String,
    DateTime, BigInteger,
    ForeignKey, Integer,
    select,
    ForeignKeyConstraint,
    PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from app.api.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="users_pkey"),
        {"schema": "public"}
    )

    id = Column(BigInteger, primary_key=True)
    full_name = Column(String)
    email = Column(String)
    password = Column(String)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    @classmethod
    def find(cls, db: Session, id):
        """

        :param db:
        :param id:
        :return:
        """

        result = db.execute(select(cls).where(cls.id == id))
        instance = result.scalars().first()

        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": f"There is no record for requested user id value: {id}"},
            )
        else:
            return instance


class UserRecovery(Base):
    __tablename__ = 'user_password_tokens'
    __table_args__ = (
        ForeignKeyConstraint(["user_id"], [
                             "public.users.id"], name="FK_user_password_tokens__users"),
        {"schema": "public"}
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("public.users.id"))
    user = relationship(User)
    code = Column(String)
    expire_date = Column(DateTime)
