import datetime
import sqlite3
import logging


logging.basicConfig(filename='face_recognizer.log', level=logging.INFO)
logger = logging.getLogger('Data Base')


def create_table():  # Создаем БД с id и именами для лиц
    conn = sqlite3.connect('Faces.sql')
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS
                  faces(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL)
                """)
    conn.commit()
    #  id, равный 0 всегда будет иметь имя 'None'
    cur.execute("""
                INSERT OR REPLACE INTO faces VALUES (0, 'None')
                """)
    conn.commit()
    conn.close()
    logger.info('['+str(datetime.datetime.now())+'] - '+'Created table named faces or it already exists')


def add_user(name):  # добавление данных ID и имени в БД
    conn = sqlite3.connect('Faces.sql')
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO faces
                  VALUES(?, ?)
                """, (None, name))
    conn.commit()
    conn.close()
    logger.info('['+str(datetime.datetime.now())+'] - '+'Added user {} in database'.format(name))


def read_data():  # Получение данных из БД
    conn = sqlite3.connect('Faces.sql')
    cur = conn.cursor()
    cur.execute("""
                SELECT * FROM faces
                """)
    data = cur.fetchall()
    answer = {}
    for i in data:
        answer.update({i[0]: i[1]})
    conn.close()
    return answer


def select_max():  # Получение максимального значения ID
    conn = sqlite3.connect('Faces.sql')
    cur = conn.cursor()
    cur.execute("""
                SELECT max(id) from faces
                """)
    answer = cur.fetchone()
    conn.close()
    return answer[0]
