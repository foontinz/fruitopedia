import pytest
from typing import Generator

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import session, sessionmaker

from fastapi.testclient import TestClient

from app.core.config import settings
from app.api.deps import get_db
from app.tests.overrider import DependencyOverrider
from app.main import app


@pytest.fixture(scope="session")
def prestart_db():
    engine = create_engine(settings.SQLALCHEMY_URI, pool_pre_ping=True)

    drop_query = text(f"DROP DATABASE IF EXISTS {settings.POSTGRES_TEST_DB}")
    create_query = text(f"CREATE DATABASE {settings.POSTGRES_TEST_DB}")

    with engine.connect() as conn:    
        conn.execution_options(isolation_level="AUTOCOMMIT").execute(drop_query)
        conn.commit()
        conn.execution_options(isolation_level="AUTOCOMMIT").execute(create_query)
        conn.commit()

    make_migrations()

    test_db_engine = create_engine(settings.SQLALCHEMY_TEST_DATABASE_URI, pool_pre_ping=True)
    sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)

    yield lambda: sessionLocal()
    session.close_all_sessions()
    test_db_engine.dispose()
    

    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT").execute(drop_query)
        conn.commit()


def make_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", str(settings.SQLALCHEMY_TEST_DATABASE_URI))
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def override_dep_db(prestart_db):
    with DependencyOverrider(app, overrides={get_db: lambda: prestart_db()}) as overrider:
        yield overrider     

@pytest.fixture(scope="module")
def get_test_db(prestart_db):
    return prestart_db()




#TODO fixtures are send to app as funcs, but not as their results. WHY?
# Use parametrization 
#TODO migrations are not affect new db. WHY?