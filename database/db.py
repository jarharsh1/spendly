import os
import sqlite3
from datetime import date

from werkzeug.security import check_password_hash, generate_password_hash

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spendly.db")
)

CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_db()
    user = conn.execute(
        "SELECT id, name, email FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return user


def verify_user(email, password):
    conn = get_db()
    user = conn.execute(
        "SELECT id, name, email, password_hash FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    if user is None or not check_password_hash(user["password_hash"], password):
        return None
    return user


def create_user(name, email, password):
    conn = get_db()
    password_hash = generate_password_hash(password)
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def seed_db():
    conn = get_db()
    existing = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()
    if existing["c"] > 0:
        conn.close()
        return

    password_hash = generate_password_hash("demo123")
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )
    user_id = cursor.lastrowid

    ym = date.today().strftime("%Y-%m")
    sample_expenses = [
        (user_id, 250.00, "Food", f"{ym}-03", "Groceries at supermarket"),
        (user_id, 450.00, "Food", f"{ym}-15", "Dinner with friends"),
        (user_id, 120.00, "Transport", f"{ym}-05", "Auto rickshaw fare"),
        (user_id, 1500.00, "Bills", f"{ym}-01", "Electricity bill"),
        (user_id, 800.00, "Health", f"{ym}-10", "Pharmacy"),
        (user_id, 600.00, "Entertainment", f"{ym}-12", "Movie tickets"),
        (user_id, 2200.00, "Shopping", f"{ym}-08", "New shoes"),
        (user_id, 300.00, "Other", f"{ym}-18", "Miscellaneous"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        sample_expenses,
    )
    conn.commit()
    conn.close()
