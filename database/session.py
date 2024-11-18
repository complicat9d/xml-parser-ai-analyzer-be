from fastapi import Depends
from typing import Annotated
from contextlib import contextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


from config import settings


db_url = (
    f"postgresql://"
    f"{settings.DATABASE_USER}:"
    f"{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOST}:"
    f"{settings.DATABASE_PORT}/"
    f"{settings.DATABASE_DB}"
)

_engine = None


def get_engine():
    global _engine
    if _engine is not None:
        return _engine

    _engine = create_engine(
        db_url,
        echo=settings.DEBUG_ENGINE,
        max_overflow=25,
    )
    return _engine


def _get_session() -> AsyncSession:
    with Session(get_engine()) as session, session.begin():
        yield session


sync_session = contextmanager(_get_session)
sync_session_dep: Session = Depends(_get_session)
session_dep = Annotated[Session, sync_session_dep]
