import os
import sqlite3


class SQLiteDB:
    """Класс для управления SQLite базой данных.

    Предоставляет функции для создания, открытия баз данных и работы с таблицами.
    """

    def __init__(self, path, filename):
        """Инициализирует новый экземпляр класса SQLiteDB.

        Args:
            path (str): Путь к директории с базой данных.
            filename (str): Название файла базы данных.
        """
        self.db_path = f"{path}/{filename}"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    @classmethod
    def create(cls, filename='database.sqlite', path=''):
        """Создает новый экземпляр базы данных и таблицу по умолчанию.

        Args:
            filename (str): Название файла базы данных.
            path (str): Путь к директории с базой данных.

        Returns:
            SQLiteDB: Экземпляр класса SQLiteDB.
        """
        if not path:
            path = os.getcwd()  # Использование текущей директории, если путь не указан
        instance = cls(path, filename)
        instance.create_default_table()  # Создаем таблицу по умолчанию
        return instance

    @classmethod
    def open(cls, filename, path=''):
        """Открывает существующий файл базы данных.

        Args:
            filename (str): Название файла базы данных.
            path (str): Путь к директории с базой данных.

        Returns:
            SQLiteDB: Экземпляр класса SQLiteDB.
        """
        if not path:
            path = os.getcwd()  # Использование текущей директории, если путь не указан
        return cls(path, filename)

    def create_default_table(self):
        """Создает таблицу по умолчанию в базе данных."""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS DefaultTable (id INTEGER PRIMARY KEY, data TEXT)")
        self.conn.commit()

    def table_exists(self, table_name):
        """Проверяет, существует ли таблица в базе данных.

        Args:
            table_name (str): Название таблицы.

        Returns:
            bool: True если таблица существует, иначе False.
        """
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        self.cursor.execute(query, (table_name,))
        return self.cursor.fetchone() is not None

    def create_table(self, table):
        """Создает новую таблицу в базе данных согласно структуре, определенной в объекте table.

        Args:
            table (Table): Объект класса Table, содержащий название и столбцы таблицы.
        """
        if not self.table_exists(table.name):
            # Создаем столбец id с типом INTEGER, который будет PRIMARY KEY и AUTOINCREMENT
            column_definitions = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
            # Добавляем остальные столбцы из объекта Table
            column_definitions.extend(
                f"{column_name} {data_type}" for column_name, data_type in table.columns.items()
            )
            columns_sql = ', '.join(column_definitions)
            sql = f"CREATE TABLE IF NOT EXISTS {table.name} ({columns_sql})"
            self.cursor.execute(sql)
            self.conn.commit()
        else:
            print(f"Table '{table.name}' already exists.")

    def __del__(self):
        """Закрывает соединение с базой данных при удалении объекта."""
        self.conn.close()


class Table:
    """Класс для управления структурой таблицы в базе данных."""

    def __init__(self, name):
        """Инициализирует новый экземпляр класса Table.

        Args:
            name (str): Название таблицы.
        """
        self.name = name
        self.columns = {}  # Словарь для хранения столбцов и их типов

    def add_column(self, column_name, data_type):
        """Добавляет новый столбец в таблицу.

        Args:
            column_name (str): Название столбца.
            data_type (str): Тип данных столбца, допустимые типы: 'TEXT', 'ANY', 'BLOB', 'INT', 'INTEGER', 'REAL'.

        Raises:
            ValueError: Если тип данных не поддерживается.
        """
        if data_type not in ['TEXT', 'ANY', 'BLOB', 'INT', 'INTEGER', 'REAL']:
            raise ValueError("Недопустимый тип данных")
        self.columns[column_name] = data_type

    def __str__(self):
        """Возвращает строковое представление объекта."""
        return f"Table: {self.name}, Columns: {self.columns}"
