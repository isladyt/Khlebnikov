from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from models.menu import MenuWindow
from models.order import OrderWindow
from models.oder_status import OrderStatusWindow
class MainWindow(QWidget):
    #Основное окно программы
    def __init__(self, user_id, user_name):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ресторан")
        self.setFixedSize(800, 600)
        self.layout = QVBoxLayout()

        self.header_label = QLabel(f"""Ресторан «У дома»
Добро пожаловать, {self.user_name}!""")
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.header_label)

        #Кнопки
        self.menu_button = QPushButton("Просмотр меню")
        self.menu_button.clicked.connect(self.open_menu)
        self.layout.addWidget(self.menu_button)

        self.order_button = QPushButton("Создание заказа")
        self.order_button.clicked.connect(self.open_order)
        self.layout.addWidget(self.order_button)

        self.status_button = QPushButton("Мои заказы")
        self.status_button.clicked.connect(self.open_order_status)
        self.layout.addWidget(self.status_button)

        self.setLayout(self.layout)

    def open_menu(self):
        self.menu_window = MenuWindow(self.user_id)
        self.menu_window.show()

    def open_order(self):
        self.order_window = OrderWindow(self.user_id)
        self.order_window.show()

    def open_order_status(self):
        self.status_window = OrderStatusWindow(self.user_id)
        self.status_window.show()