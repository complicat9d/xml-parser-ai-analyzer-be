import pytest
import redis
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from database.models import Base
from database.session import db_url
from config import settings


def test_check_db():
    if (
        settings.DATABASE_HOST not in ("localhost", "127.0.0.1", "postgres")
        or "amazonaws" in settings.DATABASE_HOST
    ):
        print(db_url)
        raise Exception("Use local database only!")


@pytest.fixture(scope="session")
def engine():
    test_check_db()

    e = create_engine(db_url, echo=False, max_overflow=25)

    try:
        with e.begin() as con:
            Base.metadata.create_all(con)

        yield e
    finally:
        with e.begin() as con:
            Base.metadata.drop_all(con)
            # alembic_version should be dropped as well, as the next time we do alembic upgrade head
            # it won't do any changes
            con.execute(text("DROP TABLE IF EXISTS alembic_version"))


@pytest.fixture
def dbsession(engine) -> Session:
    with Session(bind=engine) as session, session.begin():
        yield session


@pytest.fixture
def redis_db():
    try:
        client = redis.StrictRedis()
        assert client.ping()
        yield client
    except redis.ConnectionError as e:
        pytest.fail(f"Could not connect to Redis: {e}")


def test_redis_connection(redis_db):
    redis_db.set("test_key", "test_value")
    assert redis_db.get("test_key") == b"test_value"
    redis_db.delete("test_key")
