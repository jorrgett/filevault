from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import (
    Column, String,
    DateTime, BigInteger,
    select, Integer, ForeignKey,
    PrimaryKeyConstraint, ForeignKeyConstraint

)
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship

from app.api.base import Base
from app.api.applications.models import Application


class Type(Base):
    __tablename__ = "types"
    __table_args__ = (
        ForeignKeyConstraint(["app_id"], [
            "public.apps.id"], name="FK_FK_types__apps"),
        PrimaryKeyConstraint("id", name="apps_pkey"),
        {"schema": "public"}
    )

    id = Column(BigInteger, primary_key=True)
    app_id = Column(BigInteger, ForeignKey("public.apps.id"))
    width = Column(Integer)
    height = Column(Integer)
    name = Column(String)
    size = Column(Integer)
    file_format = Column(String)
    content_type = Column(String)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    app = relationship(Application)

    @classmethod
    def find(cls, db: Session, id):
        """

        :param db:
        :param id:
        :return:
        """
        stmt = select(cls).where(cls.id == id)
        result = db.execute(stmt)

        instance = result.scalars().first()

        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": f"There is no record for requested type id value: {id}"},
            )
        else:
            return instance
