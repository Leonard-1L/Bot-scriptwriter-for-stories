import logging
import sqlite3
from config import DB_NAME, DB_TABLE_USERS_NAME

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w"
)


def create_db(database_name=DB_NAME):
    db_path = f'{database_name}'
    connection = sqlite3.connect(db_path)
    connection.close()
    logging.info("Таблица успешно создана")


# Функция для выполнения любого sql-запроса для изменения данных
def execute_query(sql_query, data=None, db_path=f'{DB_NAME}'):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        if data:
            cursor.execute(sql_query, data)
        else:
            cursor.execute(sql_query)

        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        logging.error(f"Ошибка в функции: execute_query. Код ошибки: {e}")


# Функция для выполнения любого sql-запроса для получения данных (возвращает значение)
def execute_selection_query(sql_query, data=None, db_path=f'{DB_NAME}'):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        if data:
            cursor.execute(sql_query, data)
        else:
            cursor.execute(sql_query)
        rows = cursor.fetchall()
        connection.close()
        return rows
    except sqlite3.Error as e:
        logging.error(f"Ошибка в функции: execute_selection_query. Код ошибки: {e}")


def create_table(table_name=DB_TABLE_USERS_NAME):
    sql_query = f'CREATE TABLE IF NOT EXISTS {table_name} ' \
                f'(user_id INTEGER PRIMARY KEY, ' \
                f'subject TEXT, ' \
                f'level TEXT, ' \
                f'task TEXT, ' \
                f'answer TEXT)'
    execute_query(sql_query)


def show_column(column):
    sql_query = f"SELECT {column} FROM users;"
    res = execute_selection_query(sql_query)
    return res


def is_value_in_table(user_id, column_name, table_name=DB_TABLE_USERS_NAME):
    sql_query = f"SELECT {column_name} FROM {table_name} WHERE user_id = {user_id} AND {column_name} IS NOT NULL"
    res = execute_selection_query(sql_query)
    if res:
        return res[0][0]
    return False


def update_row_value(user_id, column_name, new_value, table_name=DB_TABLE_USERS_NAME):
    if not is_value_in_table(user_id, user_id):
        insert_row(column_name='(user_id, subject, level, task, answer)',
                   values=f'({user_id}, NULL, NULL, NULL, "Решим задачу:")')
    sql_query = f"UPDATE {table_name} SET {column_name} = '{new_value}' WHERE user_id = {user_id}"
    execute_query(sql_query)


def insert_row(column_name, values, table_name=DB_TABLE_USERS_NAME):
    sql_query = f"INSERT INTO {table_name} {column_name} VALUES {values}"
    execute_query(sql_query)
