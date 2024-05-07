import os
import sqlite3


class SQLiteDB:
    def __init__(self, path, filename):
        self.db_path = f"{path}/{filename}"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    @classmethod
    def create(cls, path='', filename='database.sqlite'):
        if not path:
            path = os.getcwd()  # Использование текущей директории, если путь не указан
        instance = cls(path, filename)
        instance.create_default_table()  # Создаем таблицу по умолчанию
        return instance

    @classmethod
    def open(cls, filename, path=''):
        if not path:
            path = os.getcwd()  # Использование текущей директории, если путь не указан
        instance = cls(path, filename)
        return instance

    def create_default_table(self):
        # Создание таблицы по умолчанию, например, с именем 'DefaultTable'
        self.cursor.execute("CREATE TABLE IF NOT EXISTS DefaultTable (id INTEGER PRIMARY KEY, data TEXT)")
        self.conn.commit()

    def create_or_update_table(self, table_name, data):
        keys = ', '.join(f"{k} {v if k != 'id' else 'INTEGER PRIMARY KEY'}" for k, v in data.items())
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({keys})")
        self.conn.commit()

    def add_row(self, table_name, data):
        keys = ', '.join(data.keys())
        values = tuple(data.values())
        placeholders = ', '.join('?' * len(data))
        self.cursor.execute(f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders})", values)
        self.conn.commit()

    def update_value(self, table_name, column_name, id, new_value):
        self.cursor.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE id = ?", (new_value, id))
        self.conn.commit()

    def update_row(self, table_name, id, data):
        updates = ', '.join(f"{k} = ?" for k in data.keys())
        self.cursor.execute(f"UPDATE {table_name} SET {updates} WHERE id = ?", (*data.values(), id))
        self.conn.commit()

    def get_row(self, table_name, id):
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?", (id,))
        row = self.cursor.fetchone()
        columns = [description[0] for description in self.cursor.description]
        return dict(zip(columns, row))

    def get_all_rows(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def __del__(self):
        self.conn.close()
