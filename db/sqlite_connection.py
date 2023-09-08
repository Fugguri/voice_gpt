import sqlite3

from models import User

class Database:
    def __init__(self, db_file) -> None:

        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def cbdt(self):
        with self.connection:
            create = """ CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER NOT NULL UNIQUE ON CONFLICT IGNORE,
                    full_name TEXT,
                    username TEXT,
                    has_access BOOLEAN DEFAULT FALSE 
                    );"""
            self.cursor.executescript(create)

    def add_user(self, user):
        with self.connection:
            self.cursor.execute(
            f"INSERT OR IGNORE INTO users( full_name, telegram_id, username) VALUES('{user.full_name}', '{user.id}', '{user.username}')")
            
    def get_user(self,telegram_id):
        with self.connection:
            c = self.connection.cursor()
            c.execute("""SELECT id, telegram_id, username, full_name,has_access
                      FROM users
                      WHERE telegram_id=?""",
                      (telegram_id,))
            res = c.fetchone()
            user = User(*res)
            return user
    
