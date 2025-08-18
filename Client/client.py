import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import *


class MainWindow(QMainWindow):
    """
    Главное окно приложения
    """

    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QGridLayout()
        central_widget.setLayout(layout)

        self.label_edit = QLabel("Введите текст:")
        self.line_edit = QLineEdit()
        self.button_post = QPushButton("Отправить")
        self.label_view = QLabel("Данные из базы:")
        self.label_per_page = QLabel("Кол-во записей на страницу:")
        self.per_page_edit = QLineEdit("10")
        self.label_num_page = QLabel("Номер страницы:")
        self.num_page_edit = QLineEdit("1")
        self.list_view = QListView()
        self.button_get = QPushButton("Получить")

        self.design_form(layout)

        self.click_count = 0

        self.button_post.clicked.connect(self.send_post_request)
        self.button_get.clicked.connect(self.get_data_from_server)

    def design_form(self, layout):
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

    def send_post_request(self):
        # TODO сделать метод отправки данных
        pass

    def get_data_from_server(self):
        # TODO сделать метод запроса данных
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
