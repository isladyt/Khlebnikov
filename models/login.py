from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from models.main_menu import MainWindow
from models.registration import RegistrationWindow
from models.admin import AdminLoginWindow
import sqlite3

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Авторизация")
        self.setFixedSize(800, 600)
        self.layout = QVBoxLayout()

        # Поля ввода
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_input)

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)

        #Кнопки
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.authenticate_user)
        self.layout.addWidget(self.login_button)

        self.register_button = QPushButton("Регистрация")
        self.register_button.clicked.connect(self.open_registration)
        self.layout.addWidget(self.register_button)

        self.admin_button = QPushButton("Войти как администратор")
        self.admin_button.clicked.connect(self.open_admin_login)
        self.layout.addWidget(self.admin_button)

        self.error_label = QLabel("")
        self.layout.addWidget(self.error_label)

        self.setLayout(self.layout)

    def authenticate_user(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()

        # Проверка email
        if not email or "@" not in email or "." not in email:
            QMessageBox.warning(self, "Ошибка", "Вы ввели некорректные данные для email.")
            return

        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Client WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.user_id, self.user_name = user
            QMessageBox.information(self, "Уведомление", f"Добро пожаловать, {self.user_name}!")
            self.main_window = MainWindow(self.user_id, self.user_name)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Вы ввели неверный e-mail или пароль.")


    def open_registration(self):
        # Открытие окна регистрации
        self.registration_window = RegistrationWindow()
        self.registration_window.show()

    def open_admin_login(self):
        #Открытие окна входа в админ. панель
        self.admin_login_window = AdminLoginWindow()
        self.admin_login_window.show()
