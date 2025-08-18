from typing import Any

from pydantic import BaseModel, field_validator, ConfigDict
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timedelta


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
    datetime: Column[DateTime] = Column(DateTime)
    click_count: Column[int] = Column(Integer)


class RecordCreate(BaseModel):
    """
    Класс - модель данных для добавления данных в таблицу

    В классе перечислены поля, которые должны быть переданы
    в запросе POST (в виде JSON)

    Валидация осуществлена с помощью @field_validator из библиотеки Pydantic
    """
    text: str
    datetime: datetime
    click_count: int

    @field_validator('text')
    def check_text(cls, value: Any) -> Any:
        """
        Валидация текста
        :param value: Полученное значение.
        :return: Значение после валидации.
        """
        if not isinstance(value, str):
            raise ValueError('Текст должен быть типа String (строка)')
        if len(value) < 1:
            raise ValueError('Текст должен содержать хотя бы 1 символ')
        return value

    @field_validator('datetime')
    def check_datetime(cls, value: Any) -> Any:
        """
        Валидация параметра datetime
        :param value: Полученное значение.
        :return: Значение после валидации.
        """
        if not isinstance(value, datetime):
            raise ValueError('Передана дата неверного формата')
        value_date = datetime.strftime(value, '%Y-%m-%d')
        now_date = datetime.strftime(datetime.now() + timedelta(days=1), '%Y-%m-%d')
        if value_date > now_date:
            raise ValueError('Не верю, чты Вы из будущего! Проверьте дату')
        return value

    @field_validator('click_count')
    def check_click_count(cls, value: Any) -> Any:
        """
        Валидация параметра click_count
        :param value: Полученное значение.
        :return: Значение после валидации.
        """
        if not isinstance(value, int):
            raise ValueError('Число нажатий на кнопку должно быть целочисленным')
        if value < 0:
            raise ValueError('Количество нажатий на кнопку не может быть меньше 1')
        return value


class RecordResponse(RecordCreate):
    """
    Класс - модель данных для передачи данных по запросу GET.

    Кроме полей, перечисленных в RecordCreate, добавляется ключ id.
    """
    id: int

    model_config = ConfigDict(from_attributes=True)
