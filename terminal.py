from DataAccess.dbHandler import *
import cryptutils
import base64
import os
from DataAccess import AccessController


user = ""


def welcome():
    print("Welcome to Secure Storage. ")
    print("Enter 1 for login, 2 for registration")
    choice = input(">> ")
    if choice == "1":
        if login():
            print("Login Successful.")
            terminal()
        else:
            print("Wrong username or password. Try Again.")
            welcome()
    elif choice == "2":
        if register():
            print("Registration Successful. Please login to the system.")
        else:
            welcome()
    else:
        print("Wrong choice! ")
        welcome()


def login():
    username = input("username: ")
    password = input("password: ")
    global user
    user = username
    return verify_user(username, password)


def register():
    username = input("Select a username: ")
    password = input("Select a password: ")
    pass_again = input("Enter password again: ")
    if Users_DB_Handler.user_exists(username):
        print("User already exists. Select another username")
        return False
    elif password == pass_again:
        print("Passwords do not match. Try again.")
        return False
    else:
        Users_DB_Handler.add_user(username, password)
        return True


def verify_user(username, password):
    real_password = Users_DB_Handler.get_user_password(username)
    return cryptutils.SHA1(real_password) == password


def terminal():
    print_help_banner()
    choice = input("> ")
    if choice == "1":
        list_accessible_files()
    elif choice == "2":
        download_file()
    elif choice == "3":
        upload_file()
    elif choice == "Q":
        quit(0)
    else:
        print("Wrong choice.")

    terminal()


def list_accessible_files():
    print("Files you can read: ")
    read_files = AccessController.get_readable_files(user)
    for file in read_files:
        print(file)

    print("Files you can write: ")
    write_files = AccessController.get_writeable_files(user)
    for file in write_files:
        print(file)


def upload_file():
    filepath = input("path of file: ")
    filename = os.path.basename(filepath)

    if Files_DB_Handler.file_exists(filename):
        if AccessController.has_write_permission(user, filename):
            Files_DB_Handler.update_file(read_from_file(filepath), filename)
            print("File is updated.")
        else:
            print("Filename already exists and you do NOT have write permission !")

    else:
        Files_DB_Handler.add_file(read_from_file(filepath), filename)

def download_file():
    filename = input("name of the file: ")

    if Files_DB_Handler.file_exists(filename):
        if AccessController.has_read_permission(user, filename):
            file_content = Files_DB_Handler.get_file_content(filename)
            write_to_file(file_content, filename)
        else:
            print("You do NOT have read permission !")

    else:
        print("There is no file with this name")


# Take base64 and write binary
def write_to_file(file_content, filename):
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(file_content))


# Take base64 and write binary
def read_from_file(filepath):
    with open(filepath, 'rb') as f:
        return base64.b64decode(f.read())


def print_help_banner():
    print("Please select: ")
    print("[1] List Accessible Files")
    print("[2] Download File")
    print("[3] Upload File")
    print("[Q] Quit")

