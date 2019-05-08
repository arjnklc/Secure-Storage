from DataAccess.dbHandler import *


def has_read_permission(username, filename):
    user_level = Users_DB_Handler.get_user_level(username)
    file_level = Files_DB_Handler.get_file_level(filename)

    

    return False


def has_write_permission(username, filename):
    user_level = Users_DB_Handler.get_user_level(username)
    file_level = Files_DB_Handler.get_file_level(filename)

    return False

def get_readable_files(username):
    pass

def get_writeable_files(username):
    pass

