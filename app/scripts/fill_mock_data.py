import json
import os

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert

from app.config import settings
from app.database.connect import metadata
from app.models import Car

engine = create_engine(settings.get_db_uri_sync)


def load_mock(override: bool = False) -> None:
    if settings.LOAD_MOCK:
        print('Inserting data to db ...')
        file_path = f'{os.path.abspath(os.curdir)}/mock_data.json'
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        with engine.begin() as connection:
            models = [
                Car
            ]

            if override:
                metadata.drop_all(bind=connection)
                metadata.create_all(bind=connection)

            for model in models:
                if values := data.get(model.__tablename__):
                    for item in values:
                        connection.execute(
                            insert(model)
                            .values(**item)
                            .on_conflict_do_update(
                                constraint=f"{model.__tablename__}_pkey",
                                set_=item,
                            )
                        )

                        if item_id := item.get("id"):
                            if isinstance(item_id, int):
                                query = text(
                                    f"select setval('{model.__tablename__}_id_seq', (select max(id) from {model.__tablename__}))"
                                )
                                connection.execute(query)
        print('Success insert mock data')


if __name__ == "__main__":
    load_mock()
