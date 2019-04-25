import sqlite3 as lite
from cryptutils import AESCipher


class Users_DB_Handler:

    def __init__(self):
        self.con = lite.connect("")
        self.cur = self.con.cursor()

    def create_table(self):
        with self.con:
            self.cur.execute("CREATE TABLE users(id INT, username TEXT, password text)")

    def add_user(self):
        with self.con:
            self.cur.execute("CREATE TABLE cars(id INT, name TEXT, price INT)")

    def get_user_password(self, username):
        return self.cur.execute('SELECT password FROM users WHERE username=?', username)

    def get_user_role(self, username):
        return self.cur.execute('SELECT role FROM users WHERE username=?', username)




class Files_DB_Handler:
    def __init__(self, table_name):
        self.con = lite.connect(table_name)
        self.cur = self.con.cursor()

    def file_exists(self, filename):
        self.cur.execute("SELECT rowid FROM files WHERE filename = ?", filename)
        data = self.cur.fetchall()
        return len(data) != 0

    def add_file(self, file_content, file_password, file_name):
        cipher = AESCipher(file_password)
        cipher.encrypt(file_content)

        self.cur.execute("INSERT INTO files VALUES(?, ?)", file_name, file_content) # TODO

    def update_file(self, new_content, file_password, file_name):
        cipher = AESCipher(file_password)
        cipher.encrypt(new_content)
        self.cur.execute("UPDATE files SET content = ? WHERE filename = ?", (new_content, file_name))


    def get_file(self, filename):
        self.cur.execute("SELECT content FROM files WHERE filename = ?", filename)

    def get_accessible_files(self, username):
        role = Users_DB_Handler().get_user_role(username)
        self.cur.execute("SELECT filename FROM files WHERE role >= ?", role)

    def validate_password(self, filename, file_password):
        # TODO get system pass from DB
        cipher = AESCipher(Key_DB_Handler.get_system_key())  # TODO

        key = self.cur.execute("SELECT key FROM files WHERE filename >= ?", filename)

        return cipher.encrypt(file_password) == key




class Access_DB_Handler:
    def __init__(self, table_name):
        self.con = lite.connect(table_name)

    def create_table(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("CREATE TABLE cars(id INT, name TEXT, price INT)")


    def add_permission(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("CREATE TABLE cars(id INT, name TEXT, price INT)")


class Key_DB_Handler:
    def __init__(self, table_name):
        self.con = lite.connect(table_name)

    def create_table(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("CREATE TABLE key(id INT, name TEXT, price INT)")


    def add_permission(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("CREATE TABLE cars(id INT, name TEXT, price INT)")



    def get_file_key(self, filename):
        return self.cur.execute("SELECT key FROM files WHERE filename = ?", filename)


    def get_system_key(self):
        return self.get_file_key("system")