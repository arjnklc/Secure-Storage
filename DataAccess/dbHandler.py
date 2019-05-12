import sqlite3 as lite
from cryptutils import AESCipher, SHA1
import enum


class Permission(enum.Enum):
    read = 1
    write = 2
    full = 3


class ConnectionProvider:

    def __init__(self):
        try:
            self.connection = lite.connect("D:\Projects\Python\db\securestorage.db")
        except lite.Error as e:
            print(e)


class Users_DB_Handler:

    def __init__(self, connection):
        self.con = connection
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        if self.con is not None:
            sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                                    id integer PRIMARY KEY,
                                                    username text NOT NULL,
                                                    password text NOT NULL,
                                                    level integer
                                                ); """
            try:
                with self.con:
                    self.cur.execute(sql_create_users_table)
            except lite.Error as e:
                print(e)
        else:
            print("Error! cannot create the database connection.")

    # Add new user to the DB. Save hash of password instead of plaintext password
    def add_user(self, username, password, level):
        user_exists = self.user_exists(username)
        if user_exists:
            print("An error occurred during user registration")
            return
        user = (username, SHA1(password), level)
        sql = ''' INSERT INTO users(username,password,level)
                      VALUES(?,?,?) '''
        self.cur.execute(sql, user)
        return self.cur.lastrowid

    def get_user_password(self, username):
        self.cur.execute("SELECT password FROM users WHERE username=?", (username,))
        password = self.cur.fetchone()
        return password[0]

    def get_user_level(self, username):
        self.cur.execute("SELECT level FROM users WHERE username=?", (username,))
        level = self.cur.fetchone()
        return level[0]

    def user_exists(self, username):
        self.cur.execute("SELECT id FROM users WHERE username=?", (username,))
        user = self.cur.fetchone()
        if user is not None:
            return True
        else:
            return False


class Files_DB_Handler:

    def __init__(self, connection):
        self.con = connection
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        if self.con is not None:
            sql_create_files_table = """ CREATE TABLE IF NOT EXISTS files (
                                                    id integer PRIMARY KEY,
                                                    filename text NOT NULL,
                                                    content text NOT NULL,
                                                    level integer,
                                                    simple_property integer,
                                                    star_property integer,
                                                    strong_star_property integer
                                                ); """
            try:
                with self.con:
                    self.cur.execute(sql_create_files_table)
            except lite.Error as e:
                print(e)
        else:
            print("Error! cannot create the database connection.")

    def file_exists(self, filename):
        self.cur.execute("SELECT id FROM files WHERE filename = ?", filename)
        data = self.cur.fetchone()
        if data is not None:
            return True
        else:
            return False

    #TODO security properties will be talked
    def add_file(self, file_content, file_password, file_name, level, security_property):
        cipher = AESCipher(file_password)
        encrypted_content = cipher.encrypt(file_content)

        file = (file_name, encrypted_content, level, security_property)
        sql = ''' INSERT INTO files(filename,content,level,security_property)
                              VALUES(?,?,?,?) '''
        self.cur.execute(sql, file)
        return self.cur.lastrowid

    def update_file(self, new_content, file_name, file_password, security_properties):
        sql = ''' UPDATE tasks
                      SET content = ? 
                      WHERE filename = ?'''
        cipher = AESCipher(file_password)
        encrypted_content = cipher.encrypt(new_content)
        self.cur.execute(sql, (encrypted_content, file_name))

    def get_file_content(self, file_name):
        self.cur.execute("SELECT content FROM files WHERE filename=?", (file_name,))
        content = self.cur.fetchone()
        return content[0]

    def get_all_file_names(self):
        self.cur.execute("select filename from files")
        files = self.cur.fetchall()
        return list(files)

    def get_accessible_files(self, username):
        level = Users_DB_Handler(self.con).get_user_level(username)
        self.cur.execute("SELECT filename FROM files WHERE level >= ?", (level,))
        files = self.cur.fetchall()
        return list(files)

    # Talk about this
    def validate_password(self, filename, file_password):
        # TODO get system pass from DB
        cipher = AESCipher(Key_DB_Handler(self.con).get_system_key())  # TODO

        key = self.cur.execute("SELECT key FROM files WHERE filename >= ?", filename)

        return cipher.encrypt(file_password) == key

    def has_simple_property(self, file_name):
        self.cur.execute("SELECT property FROM files WHERE filename=?", (file_name,))
        file_property = self.cur.fetchone()
        #return file_property[0] == File_Property.simple.value

    def has_star_property(self, file_name):
        self.cur.execute("SELECT property FROM files WHERE filename=?", (file_name,))
        file_property = self.cur.fetchone()
        #return file_property[0] == File_Property.star.value

    def has_strong_star_property(self, file_name):
        self.cur.execute("SELECT property FROM files WHERE filename=?", (file_name,))
        file_property = self.cur.fetchone()
        #return file_property[0] == File_Property.strong_star.value


class Access_DB_Handler:

    def __init__(self, connection):
        self.con = connection
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        if self.con is not None:
            sql_create_access_table = """ CREATE TABLE IF NOT EXISTS access (
                                                    id integer PRIMARY KEY,
                                                    username text,
                                                    filename text,
                                                    permission integer
                                                ); """
            try:
                with self.con:
                    self.cur.execute(sql_create_access_table)
            except lite.Error as e:
                print(e)
        else:
            print("Error! cannot create the database connection.")

    def add_permission(self, username, filename, permission):
        access = (username, filename, permission.value)
        sql = ''' INSERT INTO access(username, filename, permission)
                              VALUES(?,?,?) '''
        self.cur.execute(sql, access)
        return self.cur.lastrowid

    # Özel izinler
    def has_read_permission(self, file_name, user_name):
        self.cur.execute("SELECT permission FROM access WHERE filename=? AND username=?", (file_name,user_name))
        permission = self.cur.fetchone()
        return permission[0] == Permission.read.value

    def has_write_permission(self, file_name, user_name):
        self.cur.execute("SELECT permission FROM access WHERE filename=? AND username=?", (file_name,user_name))
        permission = self.cur.fetchone()
        return permission[0] == Permission.write.value


class Key_DB_Handler:

    def __init__(self, connection):
        self.con = connection
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
