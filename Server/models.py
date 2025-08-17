from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    """
    Декларативный класс
    """
    pass


class RecordBase(Base):
    """
    Класс данных, которые хранятся в таблице Records.
    """
    __tablename__: str = 'Records'

    id: Column[int] = Column(Integer, primary_key=True, index=True)
    text: Column[String] = Column(String, nullable=False)
    datetime: Column[datetime] = Column(TIMESTAMP)
    click_count: Column[int] = Column(Integer)


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
