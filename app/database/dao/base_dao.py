from abc import ABC

from app.database.connect import DatabaseConnect


class BaseDAO(ABC):
    def __init__(self) -> None:
        self.session = DatabaseConnect().db_connect
        self.trans = self.session.begin()

    async def __aenter__(self):
        await self.trans.__aenter__()
        return self  # type: ignore

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        await self.trans.__aexit__(exc_type, exc_val, exc_tb)
        await self.session.__aexit__(exc_type, exc_val, exc_tb)
