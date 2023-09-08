from datetime import date
import pymysql
from config.config import Config
from models import User,Character


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
            
        with self.connection.cursor() as cursor:
            create = """CREATE TABLE IF NOT EXISTS Characters
                        (id INT PRIMARY KEY AUTO_INCREMENT,
                        name TEXT,
                        description TEXT,
                        role_settings TEXT,
                        voice_id INTEGER,
                        use_count BIGINT DEFAULT 0
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


    def add_user(self, user:User):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT IGNORE INTO users (full_name, telegram_id, username) VALUES (%s, %s, %s) ",(user.full_name, user.id, user.username))
            self.connection.commit()
            self.connection.close()
            
    def add_character(self, character:Character):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT IGNORE INTO Characters (name, desctiprion, role_settings, use_count) VALUES (%s,%s, %s, %s) ",
                           (character.name,character.description,character.role_settings,character.use_count))
            self.connection.commit()
            self.connection.close()
            
            
    def get_all_characters(self):
        result = []
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM Characters""")
            res = cursor.fetchall()
            self.connection.commit()
            self.connection.close()        
            for character in res:
                result.append(Character(*character))
        return result
    
    def get_all_users(self):
        result = []
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM users""")
            res = cursor.fetchone()
            self.connection.commit()
            self.connection.close() 
            for user in res:
                result.append(User(*user))
        return result
    
    def get_character(self,id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT *
                FROM character
                WHERE id=%s""",(id,))
            res = cursor.fetchone()
            self.connection.commit()
            self.connection.close()        
            user = Character(*res)
        return user
            
    def update_character_count(self,id):
        self.connection.ping()
        with self.connection.cursor() as cursor:

            cursor.execute(
                """UPDATE Character SET use_count = use_count + 1WHERE id=%s""",(id,))
            res = cursor.fetchone()
            self.connection.commit()
            self.connection.close()        
            user = Character(*res)
        return user
            
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


if __name__ == "__main__":
    db = Database()
    from config.config import load_config
    
    config = load_config("config.json", "texts.yml")
    ch = Character(0,"Maria","test","test character",164,0)
    db.add_character(ch)