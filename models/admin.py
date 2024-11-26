from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QInputDialog, QLineEdit
from PyQt6.QtWidgets import QFileDialog, QMessageBox
import sqlite3
import pandas as pd

class AdminLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Авторизация для администратора")
        self.setFixedSize(400, 300)
        self.layout = QVBoxLayout()

        #Поля ввода
        self.email_label = QLabel("Email администратора:")
        self.email_input = QLineEdit()
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_input)

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)

        #Кнопка
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.authenticate_admin)
        self.layout.addWidget(self.login_button)

        self.error_label = QLabel("")
        self.layout.addWidget(self.error_label)

        self.setLayout(self.layout)

    def authenticate_admin(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()

        if email == "admin@ranepa.ru" and password == "admin123":
            QMessageBox.information(self, "Успех", "Добро пожаловать, Администратор!")
            self.open_admin_panel()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный email или пароль.")

    def open_admin_panel(self):
        self.admin_panel = AdminPanelWindow()
        self.admin_panel.show()
        self.close()


class AdminPanelWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Админ. панель")
        self.setFixedSize(800, 600)
        self.layout = QVBoxLayout()

        #Список заказов
        self.orders_list = QListWidget()
        self.layout.addWidget(self.orders_list)

        #Кнопки
        self.status_button = QPushButton("Изменить статус заказа")
        self.status_button.clicked.connect(self.change_order_status)
        self.layout.addWidget(self.status_button)

        self.export_button = QPushButton("Экспортировать заказы в Excel")
        self.export_button.clicked.connect(self.export_to_excel)
        self.layout.addWidget(self.export_button)

        self.setLayout(self.layout)
        self.load_orders()

    def load_orders(self):
        #Загрузка заказов из базы данных
        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, client_id, amount, status FROM OrderTable")
        self.orders = cursor.fetchall()
        conn.close()

        self.orders_list.clear()
        for order in self.orders:
            self.orders_list.addItem(
                f"Заказ #{order[0]} - Клиент {order[1]} - Сумма: {order[2]} руб. - Статус: {order[3]}")

    def change_order_status(self):
        #Изменение статуса выбранного заказа
        selected_index = self.orders_list.currentRow()
        if selected_index >= 0 and selected_index < len(self.orders):
            order_id = self.orders[selected_index][0]
            statuses = ["Принят", "Готов", "Получен"]
            new_status, ok = QInputDialog.getItem(self, "Изменение статуса", "Выберите новый статус:", statuses, 0,
                                                  False)
            if ok and new_status:
                conn = sqlite3.connect("restaurant.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE OrderTable SET status = ? WHERE id = ?", (new_status, order_id))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Успех", f"Статус заказа #{order_id} изменён на '{new_status}'.")
                self.load_orders()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ для изменения статуса.")
    def export_to_excel(self):
        #Экспортирование заказов в файл MS Excel
        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, client_id, amount, status, date FROM OrderTable")
        orders = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(orders, columns=["ID заказа", "ID клиента", "Сумма", "Статус", "Дата"])
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как", "", "Excel Files (*.xlsx)")

        if file_path:
            df.to_excel(file_path, index=False, engine="openpyxl")
            QMessageBox.information(self, "Успех", f"Заказы успешно экспортированы в файл: {file_path}")