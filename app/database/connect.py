from typing import Any

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

from app.config import settings

metadata = MetaData()


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr  # type: ignore
    def __tablename__(self) -> str:
        return self.__name__.lower()


class DatabaseConnect:
    def __init__(self):
        self.db_connect = self.async_sess()

    def async_sess(self):
        engine = create_async_engine(settings.get_db_uri, future=True, echo=False)
        async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        db_session = async_session()
        return db_session

    def sync_sess(self):
        engine = create_engine(settings.get_db_uri_sync, future=True, echo=False)
        session_fabric = sessionmaker(engine, expire_on_commit=False)
        return session_fabric
