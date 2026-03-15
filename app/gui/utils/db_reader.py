import sqlite3
from pathlib import Path
from datetime import datetime

def fetch_car_data():
    db_path = Path(__file__).resolve().parents[3] / "data" / "processed" / "cars.db"

    print(f"[DEBUG] DB path: {db_path}")

    if not db_path.exists():
        raise FileNotFoundError(f"[ERROR] Database file not found: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT title, price, link, image_url, local_image_path, brand, model, year, transmission, mileage, condition, fuel_type, location FROM cars")
    rows = cursor.fetchall()
    conn.close()

    car_data = []
    for row in rows:
        car_data.append({
            "title": row[0],
            "price": row[1],
            "link": row[2],
            "image_url": row[3],
            "local_image_path": row[4],
            "brand": row[5],
            "model": row[6],
            "year": row[7],
            "transmission": row[8],
            "mileage": row[9],
            "condition": row[10],
            "fuel_type": row[11],
            "location": row[12],
        })
    return car_data

def parse_news_date(date_str):
    """Parse date strings like 'Apr 25, 2025' into a datetime for sorting."""
    if not date_str:
        return datetime.min
    try:
        return datetime.strptime(date_str.strip(), "%b %d, %Y")
    except ValueError:
        return datetime.min

def fetch_news_data():
    db_path = Path(__file__).resolve().parents[3] / "data" / "processed" / "news.db"

    print(f"[DEBUG] DB path: {db_path}")

    if not db_path.exists():
        raise FileNotFoundError(f"[ERROR] Database file not found: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch
    cursor.execute("SELECT title, link, image_url, local_image_path, author, date, intro FROM news")
    rows = cursor.fetchall()
    conn.close()

    news_data = []
    for row in rows:
        news_data.append({
            "title": row[0],
            "link": row[1],
            "image_url": row[2],
            "local_image_path": row[3],
            "author": row[4],
            "date": row[5],
            "intro": row[6],
        })

    # Sort by parsed date, most recent first
    news_data.sort(key=lambda x: parse_news_date(x["date"]), reverse=True)

    return news_data