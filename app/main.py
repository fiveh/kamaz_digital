from fastapi import (
    FastAPI
)
from fastapi.middleware.cors import CORSMiddleware

from app.logger import get_logger
from app.routers import car
from app.scripts.fill_mock_data import load_mock

app = FastAPI(
    title="Kamaz-Digital",
    version="0.0.1",
    description="No rules - Kamaz!"
)

app.include_router(car.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def create_logs() -> None:
    get_logger(name="uvicorn.access", path="../logs/fast_api.log")


@app.on_event("startup")
def load_mock_data():
    load_mock()
