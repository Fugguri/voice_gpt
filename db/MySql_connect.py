from datetime import date
import pymysql
from config import Config
from models import User


class Database:
    def __init__(self,cfg:Config ):
        self.cfg:Config = cfg
        self.connection = pymysql.connect(
            host=self.cfg.tg_bot.host,
            user=self.cfg.tg_bot.user,
            port=self.cfg.tg_bot.port,
            password=self.cfg.tg_bot.password,
            database=self.cfg.tg_bot.database,
        )
        self.connection.autocommit(True)

    def cbdt(self):
        with self.connection.cursor() as cursor:
            create = """CREATE TABLE IF NOT EXISTS users
                        (id INT PRIMARY KEY AUTO_INCREMENT,
                        telegram_id BIGINT UNIQUE NOT NULL ,
                        full_name TEXT,
                        username TEXT,
                        has_acces BOOL DEFAULT false
                        );"""
            cursor.execute(create)
            self.connection.commit()

        # with self.connection.cursor() as cursor:
        #     create =""" CREATE TABLE IF NOT EXISTS clients
        #             (id INT PRIMARY KEY AUTO_INCREMENT,
        #             user_id INT,
        #             api_id INT,
        #             api_hash TEXT,
        #             phone TEXT NOT NULL,
        #             ai_settings TEXT,
        #             mailing_text TEXT,
        #             answers BIGINT DEFAULT 0,
        #             gs TEXT UNIQUE ,
        #             is_active BOOL DEFAULT false,
        #             FOREIGN KEY(user_id) REFERENCES users(id) )"""
        #     cursor.execute(create)
        #     self.connection.commit()


    def add_user(self, user):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT IGNORE INTO users (full_name, telegram_id, username) VALUES (%s, %s, %s) ",(user.full_name, user.id, user.username))
            self.connection.commit()
            self.connection.close()
            
            
    def get_user(self,telegram_id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT id, telegram_id, username, full_name, has_acces
                FROM users
                WHERE telegram_id=%s""",(telegram_id,))
            res = cursor.fetchone()
            self.connection.commit()
            self.connection.close()        
            user = User(*res)
        return user
