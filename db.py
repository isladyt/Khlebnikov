import sqlite3
from utils.image_utils import convert_image_to_blob

def setup_database():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    # Таблицы
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Client (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT UNIQUE,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Category (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Dish (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        kitchen TEXT,
        category_id INTEGER,
        ingredients TEXT,
        price TEXT NOT NULL,  -- Цена хранится как строка
        portion_size INTEGER,
        description TEXT,
        photo BLOB,
        FOREIGN KEY (category_id) REFERENCES Category (id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS OrderTable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT,
        amount TEXT,  -- Сумма хранится как строка
        payment_method TEXT,
        FOREIGN KEY (client_id) REFERENCES Client (id)
    )
    """)

    # Заполнение категорий
    cursor.execute("SELECT COUNT(*) FROM Category")
    if cursor.fetchone()[0] == 0:
        categories = [
            ("Салаты", "Разнообразные свежие и полезные салаты."),
            ("Основные блюда", "Горячие блюда на любой вкус."),
            ("Десерты", "Сладкие угощения."),
            ("Напитки", "Освежающие и горячие напитки.")
        ]
        cursor.executemany("INSERT INTO Category (name, description) VALUES (?, ?)", categories)

    # Заполнение блюд
    cursor.execute("SELECT COUNT(*) FROM Dish")
    if cursor.fetchone()[0] == 0:
        dishes = [
            ("Цезарь", "Европейская", 1, "Курица, салат, сыр, соус", f"{350.00:.2f}", 250, "Классический салат с курицей", convert_image_to_blob("images/caesar.jpg")),
            ("Борщ", "Русская", 2, "Свекла, капуста, картофель, мясо", f"{200.00:.2f}", 300, "Традиционный русский суп", convert_image_to_blob("images/borscht.jpg")),
            ("Тирамису", "Итальянская", 3, "Маскарпоне, кофе, бисквит", f"{400.00:.2f}", 200, "Итальянский десерт", convert_image_to_blob("images/tiramisu.jpg")),
            ("Кофе американо", "Итальянская", 4, "Кофе", f"{150.00:.2f}", 200, "Классический черный кофе", convert_image_to_blob("images/americano.jpg")),
            ("Оливье", "Русская", 1, "Картофель, колбаса, горошек, майонез", f"{300.00:.2f}", 300, "Популярный праздничный салат", convert_image_to_blob("images/olivier.jpg")),
            ("Пицца Маргарита", "Итальянская", 2, "Томат, сыр моцарелла, базилик", f"{500.00:.2f}", 400, "Классическая пицца", convert_image_to_blob("images/margherita.jpg")),
            ("Чизкейк", "Американская", 3, "Сыр, печенье, сахар", f"{450.00:.2f}", 200, "Нежный сырный десерт", convert_image_to_blob("images/cheesecake.jpg")),
            ("Чай зеленый", "Китайская", 4, "Чайный лист", f"{100.00:.2f}", 250, "Ароматный горячий напиток", convert_image_to_blob("images/green_tea.jpg"))
        ]
        cursor.executemany("""
        INSERT INTO Dish (name, kitchen, category_id, ingredients, price, portion_size, description, photo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, dishes)

    conn.commit()
    conn.close()
