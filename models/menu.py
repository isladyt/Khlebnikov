from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QListWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import sqlite3

class MenuWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Меню ресторана")
        self.setFixedSize(800, 600)

        self.layout = QVBoxLayout()

        # Заголовок
        self.header_label = QLabel("Меню ресторана")
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.header_label)

        # Выпадающий список для категорий
        self.category_dropdown = QComboBox()
        self.category_dropdown.setStyleSheet("padding: 8px; font-size: 16px;")
        self.category_dropdown.currentIndexChanged.connect(self.load_dishes)
        self.layout.addWidget(self.category_dropdown)

        # Список блюд
        self.dish_list = QListWidget()
        self.dish_list.setStyleSheet("font-size: 16px; padding: 8px;")
        self.dish_list.itemClicked.connect(self.display_dish_details)
        self.layout.addWidget(self.dish_list)

        # Фото блюда
        self.dish_image = QLabel()
        self.dish_image.setFixedSize(400, 300)
        self.dish_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.dish_image)

        # Информация о блюде
        self.dish_info_layout = QVBoxLayout()

        self.dish_name = QLabel("")
        self.dish_name.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.dish_info_layout.addWidget(self.dish_name)

        self.dish_kitchen = QLabel("")
        self.dish_info_layout.addWidget(self.dish_kitchen)

        self.dish_ingredients = QLabel("")
        self.dish_ingredients.setWordWrap(True)
        self.dish_info_layout.addWidget(self.dish_ingredients)

        self.dish_description = QLabel("")
        self.dish_description.setWordWrap(True)
        self.dish_info_layout.addWidget(self.dish_description)

        self.dish_price = QLabel("")
        self.dish_info_layout.addWidget(self.dish_price)

        self.dish_portion = QLabel("")
        self.dish_info_layout.addWidget(self.dish_portion)

        self.layout.addLayout(self.dish_info_layout)

        # Скрываем информацию о блюде до его выбора
        self.dish_image.hide()
        self.dish_name.hide()
        self.dish_kitchen.hide()
        self.dish_ingredients.hide()
        self.dish_description.hide()
        self.dish_price.hide()
        self.dish_portion.hide()

        self.load_categories()
        self.setLayout(self.layout)

    def load_categories(self):
        # Загрузка категорий из базы данных
        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Category")
        categories = cursor.fetchall()
        conn.close()

        self.category_dropdown.clear()
        self.category_dropdown.addItem("Все категории", None)
        for category in categories:
            self.category_dropdown.addItem(category[1], category[0])

    def load_dishes(self):
        # Загрузка блюд из базы данных
        category_id = self.category_dropdown.currentData()
        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()
        if category_id:
            cursor.execute("SELECT id, name FROM Dish WHERE category_id = ?", (category_id,))
        else:
            cursor.execute("SELECT id, name FROM Dish")
        self.dishes = cursor.fetchall()
        conn.close()

        self.dish_list.clear()
        for dish in self.dishes:
            self.dish_list.addItem(dish[1])  # Показываем только название блюда

    def display_dish_details(self, item):
        #Отображение фото блюд
        selected_index = self.dish_list.currentRow()
        dish_id = self.dishes[selected_index][0]

        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, kitchen, ingredients, description, price, portion_size, photo 
            FROM Dish WHERE id = ?
        """, (dish_id,))
        dish_details = cursor.fetchone()
        conn.close()

        if dish_details:
            name, kitchen, ingredients, description, price, portion_size, photo_blob = dish_details

            #Обновление текстовых полей
            self.dish_name.setText(f"Название: {name}")
            self.dish_kitchen.setText(f"Кухня: {kitchen}")
            self.dish_ingredients.setText(f"Состав: {ingredients}")
            self.dish_description.setText(f"Описание: {description}")
            self.dish_price.setText(f"Цена: {price} руб.")
            self.dish_portion.setText(f"Размер порции: {portion_size} г.")

            #Обновление фото
            pixmap = QPixmap()
            if photo_blob:
                pixmap.loadFromData(photo_blob)
                self.dish_image.setPixmap(pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio))
                self.dish_image.show()

            #Показ информации о блюде
            self.dish_name.show()
            self.dish_kitchen.show()
            self.dish_ingredients.show()
            self.dish_description.show()
            self.dish_price.show()
            self.dish_portion.show()
