from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3


def create_database() -> None:
    """
    Создаем файл БД и таблицу Records если они не были созданы
    """
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Records (
    id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    datetime TIMESTAMP NOT NULL,
    click_count INTEGER
    )
    ''')

    connection.commit()
    connection.close()


create_database()
engine = create_engine('sqlite:///database.db', echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
