import sqlite3 as lite
from cryptutils import AESCipher, SHA1


class Users_DB_Handler:

    def __init__(self):
        self.table_name = "user"
        self.con = lite.connect(self.table_name)

        self.cur = self.con.cursor()
        self.create_table()


    def create_table(self):
        with self.con:
            self.cur.execute("CREATE TABLE if not exists user(id INT, username TEXT, password text, level INT)")

    # Add new user to the DB. Save hash of password instead of plaintext password
    def add_user(self, username, password, level):
        self.cur.execute("INSERT INTO user VALUES(?, ?, ?)", (username, SHA1(password), level) )

    def get_user_password(self, username):
        return self.cur.execute('SELECT password FROM user WHERE username=?', username)

    def get_user_level(self, username):
        return self.cur.execute('SELECT role FROM user WHERE username=?', username)

    def user_exists(self, username):
        self.cur.execute("SELECT username FROM user WHERE username = ?", [username])
        data = self.cur.fetchall()
        return len(data) != 0


class Files_DB_Handler:
    def __init__(self):
        self.table_name = "file"
        self.con = lite.connect(self.table_name)
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        with self.con:
            self.cur.execute("CREATE TABLE  if not exists file(id INT, filename TEXT, content text, "
                             "simple_property INT, star_property INT, strong_star_property INT)")


    def file_exists(self, filename):
        self.cur.execute("SELECT rowid FROM files WHERE filename = ?", filename)
        data = self.cur.fetchall()
        return len(data) != 0

    def add_file(self, file_content, file_password, filename, security_properties):
        cipher = AESCipher(file_password)
        cipher.encrypt(file_content)

        self.cur.execute("INSERT INTO files VALUES(?, ?)", filename, file_content) # TODO

    def update_file(self, new_content, filename, security_properties):
        cipher.encrypt(new_content)
        self.cur.execute("UPDATE files SET content = ? WHERE filename = ?", (new_content, filename))


    def get_file_content(self, filename):
        self.cur.execute("SELECT content FROM files WHERE filename = ?", filename)

    def get_all_filenames(self):
        self.cur.execute("SELECT filename FROM files")


    def get_accessible_files(self, username):
        role = Users_DB_Handler().get_user_role(username)
        self.cur.execute("SELECT filename FROM files WHERE role >= ?", role)

    def validate_password(self, filename, file_password):
        # TODO get system pass from DB
        cipher = AESCipher(Key_DB_Handler.get_system_key())  # TODO

        key = self.cur.execute("SELECT key FROM files WHERE filename >= ?", filename)

        return cipher.encrypt(file_password) == key

    def has_simple_property(self, filename):
        return self.cur.execute("SELECT simple_property FROM files WHERE filename = ?", filename)


    def has_star_property(self, filename):
        return self.cur.execute("SELECT star_property FROM files WHERE filename = ?", filename)

    def has_strong_star_property(self, filename):
        return self.cur.execute("SELECT strong_star_property FROM files WHERE filename = ?", filename)



class Access_DB_Handler:
    def __init__(self):
        self.table_name = "access"
        self.con = lite.connect(self.table_name)
        self.cur = self.con.cursor()
        self.create_table()


    def create_table(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("CREATE TABLE  if not exists access(id INT, username TEXT, filename TEXT, permission, TEXT)")


    def add_permission(self, username, filename, permission):
        self.cur.execute("INSERT INTO access VALUES(?, ?, ?)", username, filename, permission)  # TODO

    # Özel izinler
    def has_read_permission(self, username, filename):
        perm = self.cur.execute("SELECT permission FROM access WHERE filename == ? AND username == ?", filename, username)
        return perm == "read"

    def has_write_permission(self, username, filename):
        perm = self.cur.execute("SELECT permission FROM access WHERE filename == ? AND username == ?", filename, username)
        return perm == "read"

class Key_DB_Handler:
    def __init__(self):
        self.table_name = "key"
        self.con = lite.connect(self.table_name)
        self.cur = self.con.cursor()
        self.create_table()


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