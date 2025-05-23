# Database handler
# database.py

import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("pricepulse.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_url TEXT NOT NULL,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_price(product_url, product_name, price):
    conn = sqlite3.connect("pricepulse.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO prices (product_url, product_name, price, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (product_url, product_name, price, timestamp))
    conn.commit()
    conn.close()

def get_price_history(product_url):
    conn = sqlite3.connect("pricepulse.db")
    cursor = conn.cursor()
    cursor.execute("SELECT price, timestamp FROM prices WHERE product_url = ? ORDER BY timestamp ASC", (product_url,))
    rows = cursor.fetchall()
    conn.close()
    return [{"price": row[0], "timestamp": row[1]} for row in rows]
