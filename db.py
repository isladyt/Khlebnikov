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
        price REAL NOT NULL,
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
        amount REAL,
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
            ("Цезарь", "Европейская", 1, "Курица, салат, сыр, соус", 350.0, 250, "Классический салат с курицей", convert_image_to_blob("images/caesar.jpg")),
            ("Борщ", "Русская", 2, "Свекла, капуста, картофель, мясо", 200.0, 300, "Традиционный русский суп", convert_image_to_blob("images/borscht.jpg")),
            ("Тирамису", "Итальянская", 3, "Маскарпоне, кофе, бисквит", 400.0, 200, "Итальянский десерт", convert_image_to_blob("images/tiramisu.jpg")),
            ("Кофе американо", "Итальянская", 4, "Кофе", 150.0, 200, "Классический черный кофе", convert_image_to_blob("images/americano.jpg"))
        ]
        cursor.executemany("""
        INSERT INTO Dish (name, kitchen, category_id, ingredients, price, portion_size, description, photo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, dishes)

    conn.commit()
    conn.close()
