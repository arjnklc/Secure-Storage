def has_read_permission(username, filename, users_db, files_db, access_db):
    user_level = users_db.get_user_level(username)
    file_level = files_db.get_file_level(filename)

    simple_property = files_db.has_simple_property(filename)
    strong_star_property = files_db.has_strong_star_property(filename)

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


def has_write_permission(username, filename, users_db, files_db, access_db):
    user_level = users_db.get_user_level(username)
    file_level = files_db.get_file_level(filename)

    star_property = files_db.has_star_property(filename)
    strong_star_property = files_db.has_strong_star_property(filename)

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

def get_readable_files(username, users_db, files_db, access_db):
    readable_files = []

    for filename in files_db.get_all_filenames():
        if has_read_permission(username, filename):
            readable_files.append(filename)

    return readable_files


def get_writeable_files(username, users_db, files_db, access_db):
    writeable_files = []

    for filename in files_db.get_all_filenames():
        if has_write_permission(username, filename):
            writeable_files.append(filename)

    return writeable_files



