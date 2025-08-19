from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from Server.server import app


@pytest.fixture(scope='module')
def client():
    """
    Создает клиент для тестов сервера
    :return:
    """
    return TestClient(app)


def test_create_new_record(client: TestClient) -> None:
    """
    Проверяет создание новой записи в БД
    :param client: Тестовый клиент
    """
    response = client.post('/records/create',
                           json={
                               'text': 'Test Text',
                               'datetime': "2025-08-17T17:56:00.030000",
                               'click_count': 1
                           })
    assert response.status_code == 200
    body = response.json()
    assert 'text' in body
    assert 'datetime' in body
    assert 'click_count' in body


def test_list_records(client: TestClient) -> None:
    """
    Проверяет, что в ответ на GET запрос сервер выдает список
    :param client: Тестовый клиент
    """
    response = client.get('/records/list')
    assert response.status_code == 200
    records = response.json()
    assert isinstance(records, list)


def test_invalid_per_page_value(client: TestClient) -> None:
    """
    Проверяет обработку сервером негативного сценария
    (количество записей на страницу меньше 1)
    :param client: Тестовый клиент
    """
    response = client.get('/records/list', params={'per_page': 0})
    assert response.status_code == 400
    error_detail = response.json()['detail']
    assert error_detail == "Количество элементов на страницу не может быть меньше 1"


def test_invalid_page_number(client: TestClient) -> None:
    """
    Проверяет обработку сервером негативного сценария
    (запрос на страницу с номером меньше 1)
    :param client: Тестовый клиент
    """
    response = client.get('/records/list', params={'page': 0})
    assert response.status_code == 400
    error_detail = response.json()['detail']
    assert error_detail == 'Номер страницы не может быть меньше 1'
