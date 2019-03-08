import random
import sqlite3


class Users:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             login VARCHAR(25),
                             password VARCHAR(1000),
                             user_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM uses WHERE id = ?", (str(user_id)))
        info = cursor.fetсhone()
        return info

    def add_user(self, name, password):
        user_id = random.choice(10000000)
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users
                        (login, password, user_id)
                        VALUES (?,?,?)''', (name, password, str(user_id)))
        cursor.close()
        self.connection.commit()
