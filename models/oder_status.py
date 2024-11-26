from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QListWidget
import sqlite3
class OrderStatusWindow(QWidget):
    #Окно заказов клиента
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Мои заказы")
        self.setFixedSize(800, 600)
        self.layout = QVBoxLayout()

        #Фильтр заказов по статусам
        self.status_filter = QComboBox()
        self.status_filter.addItems(["Все", "Принят", "Готов", "Получен"])
        self.status_filter.currentIndexChanged.connect(self.load_orders)
        self.layout.addWidget(self.status_filter)

        self.orders_list = QListWidget()
        self.layout.addWidget(self.orders_list)

        self.setLayout(self.layout)
        self.load_orders()

    def load_orders(self):
        #Загрузка заказов клиента из базы данных
        status = self.status_filter.currentText()
        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()

        if status == "Все":
            cursor.execute("SELECT id, status, amount FROM OrderTable WHERE client_id = ?", (self.user_id,))
        else:
            cursor.execute("""
            SELECT id, status, amount FROM OrderTable
            WHERE client_id = ? AND status = ?
            """, (self.user_id, status))

        orders = cursor.fetchall()
        conn.close()

        self.orders_list.clear()
        for order in orders:
            self.orders_list.addItem(f"Заказ #{order[0]} - {order[1]} - {order[2]} руб.")