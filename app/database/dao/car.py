from typing import List

from fastapi import HTTPException
from sqlalchemy import (
    select,
    insert,
    delete,
    update,
)
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from app.database.dao.base_dao import BaseDAO
from app.logger import get_logger
from app.models.car import Car
from app.schemas.car import (
    CarModel,
    AddCar,
    PatchCar,
)

logger = get_logger("sqlalchemy", "sqlalchemy.log")


class CarDAO(BaseDAO):
    async def create(self, fields: AddCar) -> CarModel:
        async with self.session:
            try:
                result = await self.session.scalar(
                    insert(Car).values(**fields.dict()).returning(Car)
                )
                await self.session.commit()
                result = await self.get_by_id(result)
            except SQLAlchemyError as exc:
                logger.error(exc.args)
                raise
            return CarModel.from_orm(result)

    async def delete(self, car_id: int):
        async with self.session:
            if await self.get_by_id(car_id):
                try:
                    await self.session.execute(delete(Car).where(Car.id == car_id))
                    await self.session.commit()
                except SQLAlchemyError as exc:
                    logger.error(exc.args)
                    raise

    async def update(self, fields: PatchCar, car_id) -> CarModel:

        if await self.get_by_id(car_id):
            try:
                async with self.session:
                    await self.session.scalar(
                        update(Car)
                        .values(fields.dict(exclude_unset=True))
                        .where(Car.id == car_id)
                        .returning(Car)
                    )
                    await self.session.commit()
                    return await self.get_by_id(car_id)
            except SQLAlchemyError as exc:
                logger.error(exc.args)
                raise

    async def get_list(self, is_active: bool = True) -> List[CarModel]:
        try:
            async with self.session:
                q = await self.session.execute(
                    select(Car).where(Car.is_active == is_active).order_by(Car.id)
                )
                result = q.scalars()
            return [CarModel.from_orm(r) for r in result]
        except SQLAlchemyError as exc:
            logger.error(exc.args)
            raise

    async def get_by_id(self, car_id: int) -> CarModel:
        async with self.session:
            try:
                query = await self.session.execute(
                    select(Car).where(Car.id == car_id)
                )
                result = query.scalar_one_or_none()
                if result:
                    return CarModel.from_orm(result)
            except SQLAlchemyError as exc:
                logger.error(exc.args)
                raise

            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "Транспортное средство не найдено"
                                           f" с данным id:{car_id}"
            )
