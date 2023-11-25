import sqlite3
from time import sleep

import config

def db_connect():
    global conn
    conn = sqlite3.connect(config.name_database, check_same_thread=False)
    global cursor
    cursor = conn.cursor()

def replace_dz(lesson: str, dz: str):
    cursor.execute('UPDATE dz SET {} = ? WHERE id = 1'.format(lesson), (dz,))
    conn.commit()

def replace_photo(path: str, lesson: str):
    cursor.execute('UPDATE dz SET {} = ? WHERE id = 2'.format(lesson), (path,))
    conn.commit()

def replace_url(url: str, lesson: str):
    cursor.execute('UPDATE dz SET {} = ? WHERE id = 3'.format(lesson), (url,))
    conn.commit()

def return_dz(lesson: str):
    cursor.execute('SELECT ' + lesson + ' FROM dz WHERE id = 1')
    return [str(dz[0]) for dz in cursor.fetchall()]

def return_photo(lesson: str):
    cursor.execute('SELECT ' + lesson + ' FROM dz WHERE id = 2')
    return [str(photo[0]) for photo in cursor.fetchall()]

def return_url(lesson: str):
    cursor.execute(f'SELECT {lesson} FROM dz WHERE id = 3')
    return [str(url[0]) for url in cursor.fetchall()]

def return_all_user_id():
    cursor.execute('SELECT user_id FROM users')
    return [str(user_id[0]) for user_id in cursor.fetchall()]

def remove_user(user_id: int):
    cursor.execute('DELETE FROM users WHERE user_id = ' + str(user_id))
    conn.commit()

def db_add_data(user_id: int, username: str, user_phone_number: str, user_name: str, user_surname: str, user_lang: str):
    cursor.execute('INSERT OR REPLACE INTO users (user_id, username, user_phone_number, user_name, user_surname, user_lang) VALUES (?, ?, ?, ?, ?, ?)', (user_id, username, user_phone_number, user_name, user_surname, user_lang))
    conn.commit()

def return_user_authentication(user_id: int):
    if user_id == config.admin_id_1:
        return '0'
    else:
        cursor.execute('SELECT user_id FROM users WHERE user_id = ' + str(user_id))
        if str(cursor.fetchone()) != 'None':
            return '0'
        else:
            return '1'

def db_backup():
    with open('sql_damp.txt', 'w') as f:
        for sql in conn.iterdump():
            f.write(sql)

def db_stop():
    conn.commit()
    conn.close()
