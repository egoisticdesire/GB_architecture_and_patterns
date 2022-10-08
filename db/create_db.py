import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'db_patterns.sqlite')

with sqlite3.connect(db_path) as db:

    cursor = db.cursor()

    with open('db/create_db.sql') as file:
        text = file.read()

    cursor.executescript(text)
