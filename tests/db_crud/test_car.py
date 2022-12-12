import pytest

from app import schemas
from app.database.dao.car import CarDAO


@pytest.mark.asyncio
async def test_get_car():
    car = schemas.AddCar(
        name="test_name",
        description="test_description",
        is_active=True
    )
    created_car = await CarDAO().create(fields=car)
    assert created_car in await CarDAO().get_list()


@pytest.mark.asyncio
async def test_get_car_by_id():
    car = schemas.AddCar(
        name="test_name",
        description="test_description",
        is_active=True
    )
    created_car = await CarDAO().create(fields=car)
    assert created_car == await CarDAO().get_by_id(created_car.id)


@pytest.mark.asyncio
async def test_create_car():
    car = schemas.AddCar(
        name="test_name",
        description="test_description",
        is_active=True
    )
    created_car = await CarDAO().create(fields=car)
    assert created_car.name == car.name
    assert created_car.description == car.description
    assert created_car.is_active == car.is_active


@pytest.mark.asyncio
async def test_update_car():
    car = schemas.AddCar(
        name="test_name",
        description="test_description",
        is_active=True
    )
    created_car = await CarDAO().create(fields=car)
    update_fields = schemas.PatchCar(
        name='new_test_name',
        description='new_test_description',
        is_active=False
    )
    updated_car = await CarDAO().update(fields=update_fields, car_id=created_car.id)
    assert updated_car.description == update_fields.description
    assert updated_car.is_active == update_fields.is_active


@pytest.mark.asyncio
async def test_delete_car():
    car = schemas.AddCar(
        name="test_name",
        description="test_description",
        is_active=True
    )
    created_car = await CarDAO().create(fields=car)
    assert created_car in await CarDAO().get_list()
    await CarDAO().delete(created_car.id)
    assert created_car not in await CarDAO().get_list()
