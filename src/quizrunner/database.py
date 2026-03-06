import sqlite3
from pathlib import Path
from .models import Choice, Question, TestSet

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
init_db()
def save_test(*,test):
    conn = get_connection()
    try:
      cursor = conn.cursor()
      cursor.execute(
          "INSERT INTO tests (title, description) VALUES (?, ?)",
          (test.title, test.description)
      )

      test_id = cursor.lastrowid


      for i, question in enumerate(test.questions):
          cursor.execute(
      "INSERT INTO questions (test_id, text, position) VALUES (?, ?, ?)",
      (test_id, question.text, i)
          )

          question_id = cursor.lastrowid

          for j, choice in enumerate(question.choices):
              cursor.execute(
      "INSERT INTO choices (question_id, text, is_correct, position) VALUES (?, ?, ?, ?)",
      (question_id, choice.text, choice.is_correct, j)
  )
      conn.commit()
      return test_id


    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()



def all_tests():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, created_at FROM tests ORDER BY created_at DESC")

    rows = cursor.fetchall()
    conn.close()

    return rows



def get_test_by_id(*, test_id):

    conn = get_connection()
    try:
      cursor = conn.cursor()

      cursor.execute("SELECT id, title, description FROM tests WHERE id = ?", (test_id,))

      test_row = cursor.fetchone()


      if test_row == None:
          conn.close()
          return None


      test_id_from_db, title, description = test_row

      cursor.execute("SELECT id, text FROM questions WHERE test_id = ? ORDER BY position",(test_id,))

      question_rows = cursor.fetchall()

      question_list = []

      for q_id,q_text in question_rows:

        cursor.execute("SELECT id, text, is_correct FROM choices WHERE question_id = ? ORDER BY position",(q_id,))


        choice_rows = cursor.fetchall()


        choices_list = []

        for c_id,c_text,c_correct in choice_rows:
          choice = Choice(id=c_id, text=c_text, is_correct=bool(c_correct))

          choices_list.append(choice)


        question = Question(id=q_id,text=q_text,choices=choices_list)

        question_list.append(question)

        test_obj = TestSet(id=test_id_from_db,title=title,description=description,questions=question_list)
        
      return test_obj
    finally:
        conn.close()
