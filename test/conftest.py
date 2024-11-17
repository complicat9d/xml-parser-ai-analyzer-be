import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from database.models import Base
from database.session import async_session_dep, db_url
from config import settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


def check_test_db():
    if (
        settings.DATABASE_HOST not in ("localhost", "127.0.0.1", "postgres")
        or "amazonaws" in settings.DATABASE_HOST
    ):
        print(db_url)
        raise Exception("Use local database only!")


@pytest.fixture
async def engine():
    check_test_db()

    e = create_async_engine(db_url, echo=False, max_overflow=25)

    try:
        async with e.begin() as con:
            await con.run_sync(Base.metadata.create_all)

        yield e
    finally:
        async with e.begin() as con:
            await con.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def dbsession(engine) -> AsyncSession:
    async with AsyncSession(bind=engine) as session:
        yield session


@pytest.fixture
async def test_client(dbsession) -> AsyncClient:
    from api.main import app

    def override_get_db():
        yield dbsession

    app.dependency_overrides[async_session_dep.dependency] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
