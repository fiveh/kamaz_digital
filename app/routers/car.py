from typing import List

from fastapi import (
    APIRouter,
    status,
)

from app.database.dao.car import CarDAO
from app.schemas.car import CarModel, PatchCar, AddCar

router = APIRouter(
    prefix="/v1/car", tags=["car"], responses={404: {"description": "Not found"}}
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CarModel])
async def get_all_cars(is_active: bool = True):
    return await CarDAO().get_list(is_active=is_active)


@router.get("/{car_id}/", status_code=status.HTTP_200_OK, response_model=CarModel)
async def get_one_car(car_id: int):
    return await CarDAO().get_by_id(car_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CarModel)
async def add_car(request: AddCar):
    return await CarDAO().create(request)


@router.patch("/{car_id}/", status_code=status.HTTP_200_OK, response_model=CarModel)
async def patch_car(car_id: int, request: PatchCar):
    return await CarDAO().update(request, car_id)


@router.delete("/{car_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def drop_car(car_id: int):
    return await CarDAO().delete(car_id)
