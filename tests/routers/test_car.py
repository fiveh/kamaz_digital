import pytest
from httpx import AsyncClient
from starlette import status

from app import schemas
from app.main import app


@pytest.mark.asyncio
async def test_get_car_list(car):
    async with AsyncClient(app=app, base_url="http://test.ru") as ac:
        response = await ac.get(url=f"/v1/car/")
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0
    assert car in data


async def test_get_non_active_car(car_not_active):
    async with AsyncClient(app=app, base_url="http://test.ru") as ac:
        params = {'is_active': False}
        response = await ac.get(url=f"/v1/car/", params=params)
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0
    assert car_not_active in data


async def test_car_not_exist(car, car_not_active):
    async with AsyncClient(app=app, base_url="http://test.ru") as ac:
        response = await ac.get(url=f"/v1/car/0/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_patch_car_bad_request(car):
    updated_fields = {}
    async with AsyncClient(app=app, base_url="http://test.ru") as ac:
        response = await ac.patch(url=f"/v1/car/{car.get('id')}/", json=updated_fields)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_post_car():
    car = schemas.AddCar(
        name="test_name",
        description="test_description",
        is_active=True
    ).dict()
    async with AsyncClient(app=app, base_url="http://test.ru") as ac:
        response = await ac.post(url=f"/v1/car/", json=car)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_patch_car(car):
    updated_fields = schemas.PatchCar(
        name="updated_test_name",
        description="updated_test_description",
        is_active=False
    ).dict()

    async with AsyncClient(app=app, base_url="http://test.ru") as ac:
        response = await ac.patch(url=f"/v1/car/{car.get('id')}/", json=updated_fields)
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0
    assert updated_fields.get("name") in data.values()
    assert updated_fields.get("description") in data.values()


async def test_delete_car(car):
    async with AsyncClient(app=app, base_url="http://test.ru") as ac:
        response = await ac.delete(url=f"/v1/car/{car.get('id')}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    async with AsyncClient(app=app, base_url="http://test.ru") as ac:
        response = await ac.get(url=f"/v1/car/")
    assert car not in response.json()
