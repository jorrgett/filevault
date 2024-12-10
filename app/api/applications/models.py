from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import (
    Column, String,
    DateTime, BigInteger,
    select,
    PrimaryKeyConstraint
)
from sqlalchemy.orm import Session

from app.api.base import Base


class Application(Base):
    __tablename__ = "apps"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="apps_pkey"),
        {"schema": "public"}
    )

    id = Column(BigInteger, primary_key=True)
    code = Column(String, unique=True)
    secret = Column(String)
    name = Column(String)
    bucket_name = Column(String)
    bucket_key_id = Column(String)
    bucket_secret_key = Column(String)
    bucket_region = Column(String)
    bucket_invalidation_code = Column(String)
    cloudfront_url = Column(String)
    

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
                    "message": f"There is no record for requested app id value: {id}"},
            )
        else:
            return instance
