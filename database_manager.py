import sqlite3


class DataBase:
    def __init__(self):
        conn = sqlite3.connect('Forum.db', check_same_thread=False)
        self.conn = conn
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                 username VARCHAR(20),
                                 password VARCHAR(30),
                                 favorite_themes TEXT(65535),
                                 moderation CHAR(1)
                                 )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS sections 
                                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                         title VARCHAR(100),
                                         description VARCHAR(1000)
                                         )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS topics 
                                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                         title VARCHAR(100),
                                         description TEXT(65535),
                                         section_id INTEGER
                                         )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                                                (user_id INTEGER, 
                                                topic_id INTEGER,                                                 
                                                 content TEXT(65535)
                                                 )''')
        cursor.close()
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def insert_user(self, username, password, moderation):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO users
                          (username, password,favorite_themes,moderation) 
                          VALUES (?,?,?,?)''', (username, password, "", moderation))
        cursor.close()
        self.conn.commit()

    def insert_section(self, title, description):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO sections
                          (title, description) 
                          VALUES (?,?)''', (title, description))
        cursor.close()
        self.conn.commit()

    def insert_topics(self, title, description, section_id):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO sections
                          (title, description,section_id) 
                          VALUES (?,?,?)''', (title, description, section_id))
        cursor.close()
        self.conn.commit()

    def get_favorite(self, id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?",
                       (str(id)))
        rows = cursor.fetchall()
        return rows[2]

    def update_favorite(self, id, topic_id):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE users SET favorite_themes = ? WHERE id = ?''',
                       (self.get_favorite(id) + "|" + self.get_topic_title(topic_id), str(id),))
        cursor.close()
        self.conn.commit()

    def get_topic_title(self, id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE id = ?",
                       (str(id),))
        rows = cursor.fetchall()
        return rows[0]

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


db = DataBase()
db.insert_user("vlad", "qwerty", "Y")
