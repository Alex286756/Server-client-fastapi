from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class RecordBase(Base):
    """
    Класс данных, которые хранятся в таблице Records.
    """
    __tablename__ = 'Records'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    datetime = Column(TIMESTAMP)
    click_count = Column(Integer)


class RecordCreate:
    """
    Класс - модель данных для добавления данных в таблицу

    В классе перечислены поля, которые должны быть переданы
    в запросе POST (в виде JSON)
    """
    text: str
    datetime: datetime
    click_count: int


class RecordResponse(RecordCreate):
    """
    Класс - модель данных для передачи данных по запросу GET.

    Кроме полей, перечисленных в RecordCreate, добавляется ключ id.
    """
    id: int
