from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QInputDialog, QMessageBox
from PyQt6.QtCore import Qt
import sqlite3

class OrderWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.selected_dishes = []
        self.payment_method = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Создание заказа")
        self.setFixedSize(800, 600)

        self.layout = QVBoxLayout()

        #Заголовок
        self.header_label = QLabel("Выберите блюда для заказа")
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.header_label)

        #Список доступных блюд ресторана
        self.menu = QListWidget()
        self.menu.setStyleSheet("font-size: 16px; padding: 8px;")
        self.layout.addWidget(self.menu)

        #Список заказанных блюд
        self.order_label = QLabel("Ваш заказ")
        self.order_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.order_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.order_label)

        self.order_list = QListWidget()
        self.order_list.setStyleSheet("font-size: 16px; padding: 8px;")
        self.layout.addWidget(self.order_list)

        #Кнопки
        self.add_button = QPushButton("Добавить в заказ")
        self.add_button.setStyleSheet("padding: 10px; font-size: 16px;")
        self.add_button.clicked.connect(self.add_to_order)
        self.layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Убрать из заказа")
        self.remove_button.setStyleSheet("padding: 10px; font-size: 16px;")
        self.remove_button.clicked.connect(self.remove_from_order)
        self.layout.addWidget(self.remove_button)

        self.payment_button = QPushButton("Выбрать способ оплаты")
        self.payment_button.setStyleSheet("padding: 10px; font-size: 16px;")
        self.payment_button.clicked.connect(self.choose_payment_method)
        self.layout.addWidget(self.payment_button)

        self.submit_button = QPushButton("Оформить заказ")
        self.submit_button.setStyleSheet("padding: 10px; font-size: 16px;")
        self.submit_button.clicked.connect(self.submit_order)
        self.layout.addWidget(self.submit_button)

        self.load_menu()
        self.setLayout(self.layout)

    def load_menu(self):
        #Загрузка блюд из базы данных
        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM Dish")
        self.dishes = cursor.fetchall()
        conn.close()

        self.menu.clear()
        for dish in self.dishes:
            # Отображаем название и цену блюда
            self.menu.addItem(f"{dish[1]} - {dish[2]} руб.")

    def add_to_order(self):
        #Добавление блюда в заказ
        try:
            selected_index = self.menu.currentRow()
            if selected_index >= 0 and selected_index < len(self.dishes):
                dish = self.dishes[selected_index]
                dish_id, name, price = dish
                self.selected_dishes.append((dish_id, name, price))  #Добавляем в список заказов
                self.order_list.addItem(f"{name} - {price} руб.")  #Обновляем графический список
                QMessageBox.information(self, "Уведомление", f"Блюдо '{name}' добавлено в заказ!")
            else:
                QMessageBox.warning(self, "Ошибка", "Выберите блюдо из списка.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def remove_from_order(self):
        #Удаление блюда из заказа
        try:
            selected_index = self.order_list.currentRow()
            if selected_index >= 0 and selected_index < len(self.selected_dishes):
                removed_dish = self.selected_dishes.pop(selected_index)
                self.order_list.takeItem(selected_index)  #Удаляем из графического списка
                QMessageBox.information(self, "Уведомление", f"Блюдо '{removed_dish[1]}' удалено из заказа.")
            else:
                QMessageBox.warning(self, "Ошибка", "Выберите блюдо, которое хотите удалить из заказа.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def choose_payment_method(self):
        #Выбор одного из способов оплаты
        try:
            payment_methods = ["Наличные", "Карта", "Онлайн"]
            selected_method, ok = QInputDialog.getItem(self, "Способ оплаты", "Выберите способ оплаты:", payment_methods, 0, False)
            if ok and selected_method:
                self.payment_method = selected_method
                QMessageBox.information(self, "Уведомление", f"Вы выбрали: {selected_method}")
            else:
                QMessageBox.warning(self, "Ошибка", "Вы не выбрали способ оплаты.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def submit_order(self):
        #Оформление заказа
        try:
            if not self.selected_dishes:
                QMessageBox.warning(self, "Ошибка", "Список заказа пуст.")
                return

            if not self.payment_method:
                QMessageBox.warning(self, "Ошибка", "Выберите способ оплаты.")
                return

            total_amount = sum(float(dish[2]) for dish in self.selected_dishes)

            #Запись заказа в базу данных
            conn = sqlite3.connect("restaurant.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO OrderTable (client_id, amount, status, payment_method)
                VALUES (?, ?, ?, ?)
            """, (self.user_id, f"{total_amount:.2f}", "Принят", self.payment_method))
            conn.commit()

            QMessageBox.information(self, "Уведомление", f"Ваш заказ на сумму {total_amount:.2f} руб успешно оформлен!")
            self.selected_dishes = []
            self.order_list.clear()  # Очистка графического списка заказов
            self.payment_method = None

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось оформить заказ: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла непредвиденная ошибка: {str(e)}")
        finally:
            if 'conn' in locals() and conn:
                conn.close()
