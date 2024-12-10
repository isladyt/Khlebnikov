from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import sqlite3

class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Регистрация")
        self.setFixedSize(800, 600)
        self.layout = QVBoxLayout()

        self.name_label = QLabel("Имя:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.phone_label = QLabel("Телефон:")
        self.phone_input = QLineEdit()
        self.layout.addWidget(self.phone_label)
        self.layout.addWidget(self.phone_input)

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_input)

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)

        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.register_client)
        self.layout.addWidget(self.register_button)

        self.setLayout(self.layout)

    def register_client(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()

        # Проверка имени
        if not name or not name.replace(" ", "").isalpha():
            QMessageBox.warning(self, "Ошибка", "Поле «Имя» должно содержать только буквы и не быть пустым.")
            return

        # Проверка телефона
        if not phone or not phone.isdigit():
            QMessageBox.warning(self, "Ошибка", "Поле «Телефон» должно содержать только цифры.")
            return

        # Проверка email
        if not email or "@" not in email or "." not in email:
            QMessageBox.warning(self, "Ошибка", "Вы ввели некорректные данные для email.")
            return

        # Проверка пароля
        if not password or len(password) < 8:
            QMessageBox.warning(self, "Ошибка", "Пароль должен содержать не менее 8 символов.")
            return

        # Сохранение пользователя в базу данных
        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Client (name, phone, email, password)
                VALUES (?, ?, ?, ?)
            """, (name, phone, email, password))
            conn.commit()
            QMessageBox.information(self, "Уведомление", "Регистрация успешна!")
            self.close()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким email или телефоном уже существует.")
        finally:
            conn.close()
