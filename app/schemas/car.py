from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class AddCar(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True


class PatchCar(AddCar):
    description: Optional[str]
    is_active: Optional[bool]


class CarModel(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool
    created_at: Optional[Union[str, datetime]]

    class Config:
        orm_mode = True
