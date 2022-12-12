import asyncio

import pytest
from alembic.config import Config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from alembic import command
from app import schemas
from app.config import settings
from app.database.dao.car import CarDAO


def pytest_sessionstart(session):
    config = Config(file_="alembic.ini")
    command.upgrade(config, "head")


def pytest_sessionfinish(session, exitstatus):
    config = Config(file_="alembic.ini")
    command.downgrade(config, "base")


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


TestingSession = sessionmaker(bind=create_async_engine(settings.get_db_uri),
                              autocommit=False, autoflush=False,
                              class_=AsyncSession)


@pytest.fixture(scope="session")
def db():
    return TestingSession()


@pytest.fixture
async def car() -> dict:
    car = schemas.AddCar(
        name="test_name",
        description="test_description",
        is_active=True
    )
    car = await CarDAO().create(car)
    car = schemas.CarModel(**car.dict())
    car.created_at = car.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
    return car.dict()


@pytest.fixture
async def car_not_active() -> dict:
    car = schemas.AddCar(
        name="other_test_name",
        description="other_test_description",
        is_active=False
    )
    car = await CarDAO().create(car)
    car = schemas.CarModel(**car.dict())
    car.created_at = car.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
    return car.dict()
