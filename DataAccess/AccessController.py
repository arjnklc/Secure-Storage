from DataAccess.dbHandler import *


access_db = Access_DB_Handler()


def has_read_permission(username, filename):
    user_level = Users_DB_Handler.get_user_level(username)
    file_level = Files_DB_Handler.get_file_level(filename)

    simple_property = Files_DB_Handler.has_simple_property(filename)
    strong_star_property = Files_DB_Handler.has_strong_star_property(filename)

    # Special permission check
    if access_db.has_read_permission(username, filename):
        return True

    if simple_property:
        if file_level > user_level:
            return False
    if strong_star_property:
        if user_level != file_level:
            return False

    return True


def has_write_permission(username, filename):
    user_level = Users_DB_Handler.get_user_level(username)
    file_level = Files_DB_Handler.get_file_level(filename)

    star_property = Files_DB_Handler.has_star_property(filename)
    strong_star_property = Files_DB_Handler.has_strong_star_property(filename)

    # Special permission check
    if access_db.has_write_permission(username, filename):
        return True

    if star_property:
        if file_level < user_level:
            return False
    if strong_star_property:
        if user_level != file_level:
            return False

    return True

def get_readable_files(username):
    readable_files = []

    for filename in Files_DB_Handler.get_all_filenames():
        if has_read_permission(username, filename):
            readable_files.append(filename)

    return readable_files


def get_writeable_files(username):
    writeable_files = []

    for filename in Files_DB_Handler.get_all_filenames():
        if has_write_permission(username, filename):
            writeable_files.append(filename)

    return writeable_files



