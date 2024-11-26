import sys
from PyQt6.QtWidgets import QApplication
from db import setup_database
from models.login import LoginWindow
from utils.styles import APP_STYLE

if __name__ == "__main__":
    setup_database()  # Инициализация базы данных
    app = QApplication(sys.argv)

    #Применение стиля к приложению
    app.setStyleSheet(APP_STYLE)

    #Запуск окна авторизации
    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec())
