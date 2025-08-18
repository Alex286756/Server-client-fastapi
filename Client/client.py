import sys
from datetime import datetime
from typing import Any

from PySide6 import QtWidgets
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import *
import requests
from requests import Response


class MainWindow(QMainWindow):
    """
    Главное окно приложения
    """

    def __init__(self):
        super().__init__()

        central_widget: QWidget = QWidget()
        self.setCentralWidget(central_widget)
        layout: QGridLayout = QtWidgets.QGridLayout()
        central_widget.setLayout(layout)

        self.label_edit: QLabel = QLabel("Введите текст:")
        self.line_edit: QLineEdit = QLineEdit()
        self.button_post: QPushButton = QPushButton("Отправить")
        self.label_view: QLabel = QLabel("Данные из базы:")
        self.label_per_page: QLabel = QLabel("Кол-во записей на страницу:")
        self.per_page_edit: QLineEdit = QLineEdit("10")
        self.label_num_page: QLabel = QLabel("Номер страницы:")
        self.num_page_edit: QLineEdit = QLineEdit("1")
        self.list_view: QListView = QListView()
        self.button_get: QPushButton = QPushButton("Получить")

        self.design_form(layout)

        self.click_count: int = 0

        self.button_post.clicked.connect(self.send_post_request)
        self.button_get.clicked.connect(self.get_data_from_server)

    def design_form(self, layout: QGridLayout) -> None:
        """
        Расположение виджетов на форме
        :param layout: Родительский layout для виджетов
        """
        layout.addWidget(self.label_edit, 0, 0)
        layout.addWidget(self.line_edit, 0, 1)
        layout.addWidget(self.button_post, 1, 0, 1, 2)
        layout.addWidget(self.label_view, 2, 0)
        layout.addWidget(self.label_per_page, 3, 0)
        layout.addWidget(self.per_page_edit, 3, 1)
        layout.addWidget(self.label_num_page, 3, 2)
        layout.addWidget(self.num_page_edit, 3, 3)
        layout.addWidget(self.list_view, 4, 0, 1, 2)
        layout.addWidget(self.button_get, 5, 0, 1, 2)

    def send_post_request(self) -> None:
        """
        Отправка текста в базу данных
        """
        self.click_count += 1
        data_to_send: dict[str: str | int] = {
            "text": self.line_edit.text().strip(),
            "datetime": datetime.now().strftime('YYYY-MM-DDTHH:MM:SS.SSS'),
            "click_count": self.click_count
        }

        try:
            requests.post('http://localhost:8000/records/create/', json=data_to_send)
        except requests.exceptions.ConnectionError:
            message_box = QMessageBox(self)
            message_box.setWindowTitle('Ошибка отправки POST-запроса')
            message_box.setText('Ошибка при подключении к серверу')
            message_box.exec()
        except Exception as exception:
            message_box = QMessageBox(self)
            message_box.setWindowTitle('Ошибка отправки POST-запроса')
            message_box.setText(f'{exception}')
            message_box.exec()

    def get_data_from_server(self) -> None:
        """
        Получение записей из базы данных
        """
        try:
            requests_text: str = (f'http://localhost:8000/records/list?page='
                                  f'{self.num_page_edit.text()}&per_page={self.per_page_edit.text()}')
            response: Response = requests.get(requests_text)

            received_data: Any = response.json()

            items: list[str] = [(f'id = {item['id']}, text = "{item['text']}", date&time = {item['datetime']},'
                                 f'click on button: {item['click_count']}') for item in received_data]
            model: QStandardItemModel = QStandardItemModel()

            for item in items:
                std_item = QStandardItem(item)
                model.appendRow(std_item)
            self.list_view.setModel(model)
        except requests.exceptions.ConnectionError:
            message_box = QMessageBox(self)
            message_box.setWindowTitle('Ошибка отправки GET-запроса')
            message_box.setText('Ошибка при подключении к серверу')
            message_box.exec()
        except Exception as exception:
            message_box = QMessageBox(self)
            message_box.setWindowTitle('Ошибка отправки GET-запроса')
            message_box.setText(f'{exception}')
            message_box.exec()


if __name__ == "__main__":
    app: QApplication = QtWidgets.QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    sys.exit(app.exec())
