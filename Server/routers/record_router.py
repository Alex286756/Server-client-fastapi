import math
from typing import Any
from fastapi import APIRouter, HTTPException

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
async def list_all(page: int = 1, per_page: int = 10):
    """
    Получение списка элементов с поддержкой постраничной навигации.
    :param page: Номер страницы
    :param per_page: Количество записей на странице
    :return: Список элементов
    """
    if per_page < 1:
        raise HTTPException(status_code=400, detail="Количество элементов на страницу не может быть меньше 1")
    if page < 1:
        raise HTTPException(status_code=400, detail="Номер страницы не может быть меньше 1")

    with SessionLocal() as session:
        skip = (page - 1) * per_page
        total_count = session.query(RecordBase).count()
        max_pages = math.ceil(total_count / per_page) if total_count > 0 else 1

        if page > max_pages:
            raise HTTPException(status_code=400, detail="Указан неверный номер страницы")

        result = session.query(RecordBase).offset(skip).limit(per_page).all()
        return result
