import sqlite3
from pathlib import Path

def create_car_connection():
    db_path = Path(__file__).resolve().parents[2] / "data" / "processed" / "cars.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=10)  # wait up to 10 seconds for lock
    return conn
def create_car_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            price REAL,
            link TEXT,
            local_image_path TEXT,
            brand TEXT,
            model TEXT,
            year INTEGER,
            transmission TEXT,
            mileage TEXT,
            condition TEXT,
            fuel_type TEXT,
            location TEXT,
            image_url TEXT,
            UNIQUE(title, link)
        );
    ''')
    conn.commit()
    


def insert_car_data(conn, cars):
    cursor = conn.cursor()

    for car in cars:
        cursor.execute("""
            INSERT OR IGNORE INTO cars (
                title, price, link, image_url, local_image_path,
                brand, model, year, transmission, mileage,
                condition, fuel_type, location
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            car["title"], car["price"], car["link"],
            car["image_url"], car["local_image_path"],
            car["brand"], car["model"], car["year"],
            car["transmission"], car["mileage"],
            car["condition"], car["fuel_type"], car["location"]
        ))
    conn.commit()

def load_cars(transformed_data):
    conn = create_car_connection()
    create_car_table(conn)
    insert_car_data(conn, transformed_data)
    conn.close()
    
    print("[INFO] Data loaded into SQLite database.")
    print(f"[INFO] DB successfully created at {Path(__file__).resolve().parents[2] / 'data' / 'processed' / 'cars.db'}")

def create_news_connection():
    db_path = Path(__file__).resolve().parents[2] / "data" / "processed" / "news.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=10)
    return conn

def create_news_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            image_url TEXT,
            local_image_path TEXT,
            author TEXT,
            date TEXT,
            intro TEXT,
            UNIQUE(title, link)
        );
    ''')
    conn.commit()

def insert_news_data(conn, news_data):
    cursor = conn.cursor()

    for article in news_data:
        cursor.execute("""
            INSERT OR IGNORE INTO news (
                title, link, image_url, local_image_path,
                author, date, intro
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            article["title"], article["link"],
            article["image_url"], article["local_image_path"],
            article["author"], article["date"], article["intro"]
        ))

    conn.commit()

def load_news(transformed_news):
    conn = create_news_connection()
    create_news_table(conn)
    insert_news_data(conn, transformed_news)
    conn.close()

    print("[INFO] News data loaded into SQLite database.")
    print(f"[INFO] DB successfully updated at {Path(__file__).resolve().parents[2] / 'data' / 'processed' / 'news.db'}")
