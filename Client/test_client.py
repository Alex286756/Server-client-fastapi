import sys
from datetime import datetime
from unittest.mock import Mock, patch
import pytest
from PySide6.QtWidgets import QApplication, QGridLayout
from client import MainWindow


@pytest.fixture(scope="session")
def qt_app() -> QApplication:
    """
    Инициализации приложения для тестов
    """
    app: QApplication = QApplication(sys.argv)
    yield app
    app.quit()


@pytest.fixture
def main_window(qt_app: QApplication) -> MainWindow:
    """
    Создает экземпляр главного окна для тестов
    """
    return MainWindow()


def test_design_form(main_window: MainWindow) -> None:
    """
    Проверяет правильное расположение элементов на форме.
    """
    grid_layout: QGridLayout = main_window.layout

    # Проверяем позиции элементов
    assert grid_layout.itemAtPosition(0, 0).widget() == main_window.label_edit
    assert grid_layout.itemAtPosition(0, 1).widget() == main_window.line_edit
    assert grid_layout.itemAtPosition(1, 0).widget() == main_window.button_post
    assert grid_layout.itemAtPosition(2, 0).widget() == main_window.label_view
    assert grid_layout.itemAtPosition(3, 0).widget() == main_window.label_per_page
    assert grid_layout.itemAtPosition(3, 1).widget() == main_window.per_page_edit
    assert grid_layout.itemAtPosition(3, 2).widget() == main_window.label_num_page
    assert grid_layout.itemAtPosition(3, 3).widget() == main_window.num_page_edit
    assert grid_layout.itemAtPosition(4, 0).widget() == main_window.list_view
    assert grid_layout.itemAtPosition(5, 0).widget() == main_window.button_get


@patch('requests.post')
def test_method_for_send_post_request_to_server(mock_post, main_window: MainWindow) -> None:
    """
    Тестирует метод отправки POST-запроса.
    """
    main_window.line_edit.setText('Test Text')
    main_window.send_post_request()
    mock_post.assert_called_once_with(
        'http://localhost:8000/records/create/',
        json={
            'text': 'Test Text',
            'datetime': datetime.now().strftime('YYYY-MM-DDTHH:MM:SS.SSS'),
            'click_count': 1
        })


@patch('requests.get')
def test_method_for_get_data_from_server(mock_get, main_window: MainWindow) -> None:
    """
    Тестирует метод получения данных с сервера.
    """
    expected_response: list[dict[str: int | str]] = [{
        'id': 1,
        'text': 'test',
        'datetime': '2025-08-18T12:18:00.00000',
        'click_count': 1
    }]
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = expected_response
    main_window.num_page_edit.setText('1')
    main_window.per_page_edit.setText('10')
    main_window.get_data_from_server()
    mock_get.assert_called_once_with('http://localhost:8000/records/list?page=1&per_page=10')
