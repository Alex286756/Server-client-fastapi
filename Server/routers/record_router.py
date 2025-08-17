from typing import Any
from fastapi import APIRouter

from Server.models.record_model import RecordCreate, RecordBase
from Server.repositories.my_db import SessionLocal

router = APIRouter(prefix="/records")


@router.post("/create")
async def create(record: RecordCreate) -> Any:
    """
    Создание новой записи в таблице Records.
    :param record: Данные новой записи
    :return: Информация о новой записи
    """
    new_record = RecordBase(**record.model_dump())
    with SessionLocal() as session:
        session.add(new_record)
        session.commit()
        session.refresh(new_record)
        return new_record


@router.get('/list')
async def list_all():
    return "TODO list_all"
