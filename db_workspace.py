# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime


class DataBase:
    def __init__(self, conn):
        self.conn = conn
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                 username VARCHAR(20),
                                 password VARCHAR(30),
                                 favorite_themes TEXT(65535),
                                 question VARCHAR(80),
                                 answer VARCHAR(80)
                                 
                                 )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS sections 
                                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                         title VARCHAR(100),
                                         description VARCHAR(1000),
                                         link VARCHAR(20),
                                         imgpath VARCHAR(20)
                                         )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS topics 
                                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                         section_id INTEGER,
                                         title VARCHAR(100),
                                         description TEXT(65535),
                                         author VARCHAR(20),                                         
                                         date VARCHAR(80),
                                         messages INTEGER,
                                         views INTEGER
                                         )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                                                (user_id INTEGER, 
                                                topic_id INTEGER,                                                 
                                                 content TEXT(65535),
                                                 date VARCHAR(80)
                                                 )''')
        cursor.close()
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def get_usernames(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return [i[1] for i in rows]

    def insert_user(self, username, password, question, answer):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO users
                          (username, password,favorite_themes,question,answer) 
                          VALUES (?,?,?,?,?)''', (username, password, "", question, answer))
        cursor.close()
        self.conn.commit()

    def insert_section(self, title, description, link, img_path):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO sections
                          (title, description, link,imgpath) 
                          VALUES (?,?,?,?)''', (title, description, link, img_path))
        cursor.close()
        self.conn.commit()

    def insert_topic(self, section_id, title, description, author, date):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO topics
                          (section_id, title, description,author,date,messages,views) 
                          VALUES (?,?,?,?,?,?,?)''', (section_id, title, description, author, date, 0, 0))
        cursor.close()
        self.conn.commit()

    def get_favorite(self, id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?",
                       (str(id)))
        rows = cursor.fetchall()
        return rows[2]

    def update_favorite(self, id, topic_id):
        pass

    def get_topics_info(self, section_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE section_id = ?",
                       (str(section_id),))
        rows = cursor.fetchall()
        return rows

    def plus_view(self, topic_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE id = ?",
                       (str(topic_id),))
        row = int(cursor.fetchone()[-1])
        cursor.execute('''UPDATE topics SET views = ? WHERE id = ?''', (str(row+1), str(topic_id),))
        cursor.close()
        self.conn.commit()

    def get_sections_info(self, title=False):
        cursor = self.conn.cursor()
        if title:
            cursor.execute("SELECT * FROM sections WHERE link = ?",
                           (title,))
            row = cursor.fetchone()
            print(row)
            return row
        else:
            cursor.execute("SELECT * FROM sections")
        rows = cursor.fetchall()
        return [i[1:] for i in rows]

    def exists(self, user_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM news WHERE user_name = ?",
                       (user_name))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get_all_themes(self, section_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE section_id = ?",
                       (str(section_id)))
        rows = cursor.fetchall()
        return rows

    def return_section_id(self, title):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sections WHERE title = ?",
                       (title))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def delete(self, id):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ?''', (str(id)))
        cursor.close()
        self.conn.commit()


if __name__ == '__main__':
    db = DataBase(sqlite3.connect('forum.db', check_same_thread=False))
    db.insert_section("Музыка", "Все о музыке.", "music", "static/Музыка.jpg")
    db.insert_section("Книги", "Все о книгах.", "books", "static/Книги.jpg")
    db.insert_section("Спорт", "Все о спорте.", "sport", "static/Спорт.jpg")
    db.insert_section("Кинематограф", "Все о кинематографе.", "cinema", "static/Кинематограф.jpg")
    db.insert_section("Автомобили", "Все об автомобилях.", "cars", "static/Автомобили.jpg")
    db.insert_section("Политика", "Все о политике", "politics", "static/Политика.jpg")
    db.insert_topic(1, "Моцарт", "Моцарт прекрасен!Что вы думаете о нем?", "Vladislav",
                    datetime.now().strftime('%d.%m.%Y %H:%M'))
