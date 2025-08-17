from typing import Any

from fastapi import FastAPI, Depends
import uvicorn

from Server.models import RecordCreate, RecordBase
from db import SessionLocal

app: FastAPI = FastAPI()


def get_db() -> GeneratorExit:
    """
    Получаем доступ к базе данных
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create")
async def create(record: RecordCreate, db=Depends(get_db)) -> Any:
    """
    Создание новой записи в таблице Records.
    :param record: Данные новой записи
    :param db: Указатель для работы с БД
    :return: Информация о новой записи
    """
    new_record = RecordBase(**record.model_dump())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@app.get('/list')
async def list_all():
    return "TODO list_all"


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
