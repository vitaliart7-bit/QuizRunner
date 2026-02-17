import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".quizrunner" / "quiz.db"

def get_connection():
    """Возвращает соединение с БД, создавая папку при необходимости."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    """Создаёт таблицы, если их нет."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                position INTEGER,
                FOREIGN KEY (test_id) REFERENCES tests (id) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS choices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                is_correct BOOLEAN NOT NULL,
                position INTEGER,
                FOREIGN KEY (question_id) REFERENCES questions (id) ON DELETE CASCADE
            )
        """)
        conn.commit()
