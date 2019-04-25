from DataAccess.dbHandler import *
import cryptutils
import base64
import os


def login():
    print("username:")
    username = input()
    print("password:")
    password = input()
    verify_user(username, password)


def verify_user(username, password):
    real_password = Users_DB_Handler.get_user_password(username)
    return cryptutils.SHA1(real_password) == password


def list_accessible_files():
    pass


def upload_file():
    filepath = input("path of file: ")
    filename = os.path.basename(filepath)
    file_password = input("give the password: ")

    if Files_DB_Handler.file_exists(filename):

        if Files_DB_Handler.validate_password(filename, file_password):
            Files_DB_Handler.update_file(read_from_file(filepath), file_password)

        else:
            print("parola yanlış")

    else:
        Files_DB_Handler.add_file(read_from_file(filepath), file_password)


# Take base64 and write binary
def write_to_file(file_content, filename):
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(file_content))


# Take base64 and write binary
def read_from_file(filepath):
    with open(filepath, 'rb') as f:
        return base64.f.read()


def download_file():
    print("name of file: ")
    filename = input()
    if Files_DB_Handler.file_exists(filename):
        print("give the password: ")
        file_password = input()

        file = Files_DB_Handler.get_file(filename, file_password)
        write_to_file(file, filename)
    else:
        print("there is no file with this name")


def help_banner():
    print("yardim")