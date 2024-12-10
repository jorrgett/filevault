
from typing import Any

from fastapi import HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import as_declarative, declared_attr, Session


@as_declarative()
class BaseReadOnly:
    id: Any
    __name__: str
    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

    def save(self, db: Session = Depends(get_db)):
        """

        :param db: Session = Depends(get_db):
        :return:
        """
        try:
            db.add(self)
            return db.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                    'message': repr(ex)}) from ex

    def delete(self, db: Session = Depends(get_db)):
        """

        :param session: Session = Depends(get_db):
        :return:
        """
        try:
            db.delete(self)
            db.commit()
            return True
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                    'message': repr(ex)}) from ex

    def update(self, db: Session, **kwargs):
        """

        :param db
        :param kwargs
        :return:
        """
        try:
            for k, v in kwargs.items():
                setattr(self, k, v)
            return db.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                    'message': repr(ex)}) from ex

    def save_or_update(self, db: Session):
        try:
            db.add(self)
            return db.commit()
        except IntegrityError as exception:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(exception),
            ) from exception
        finally:
            db.close()
