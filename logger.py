import random
import sys
from datetime import datetime
import sqlite3

# description
# logger.py is a module that contains the functions to log errors
# into a sqlite database file.

class LoggingHandler(object):

    @classmethod
    def __init__(cls, logging_name, db_file:str="logs.db", table_name: str="logs"):
        """
        Initialize the logger.
        Args:
            logging_name (str): The name of the logger. This is used to create a table in the database to store the logs for the logger. 
        """
        cls.logging_name = logging_name
        cls.connector = sqlite3.connect('logs.db', check_same_thread=False)
        cls.cursor = cls.connector.cursor()
        cls.cursor.execute("""CREATE TABLE IF NOT EXISTS logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date DATETIME,
            level TEXT,
            message TEXT,
            path TEXT,
            line INTEGER,
            function TEXT,
            code TEXT
        )""")
        cls.connector.commit()

    @classmethod
    def log_error(cls, error: Exception):
        """
        Logs an error into the database.
        Args:
            error (Exception): The error to log, must be an exception object.
        """
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_code = cls.generate_error_codes()
        cls.connector.execute('''INSERT INTO logs (name,date, level, message, path, line, function, code) VALUES (?,?,?,?,?,?,?,?)''', (
            cls.logging_name, datetime.now(), 'ERROR', str(error), filename, line_number, exception_traceback.tb_frame.f_code.co_name, error_code))
        cls.connector.commit()
        print(error)
        return f"{cls.logging_name}:{error_code}"

    @classmethod
    def get_logs(cls, BY: str = all, value: str = None, page: int = 0, limit: int = 10, sort_by: str = 'date', descending: bool = True):
        """
        Gets the logs from the database.
        Args:
            BY (str): Type of the logs to be returned (all, name, level, message, path, line, function, code)
            value (str): Value of the log to be returned, depends on the BY parameter.
            page (int): Page number of the logs to be returned, default is 0.
            limit (int): Number of logs to be returned, default is 10.
            sort_by (str): Column to be sorted by (date, name, level, message, path, line, function, code)
            descending (bool): If the logs should be sorted in descending order.
        """
        if BY == 'all':
            cls.cursor.execute(
                f'''SELECT * FROM logs ORDER BY {sort_by} {'DESC' if descending else 'ASC'} LIMIT {limit} OFFSET {page * limit}''')
        elif BY in ['name', 'level', 'message', 'path', 'line', 'function', 'code']:
            cls.cursor.execute(
                f'''SELECT * FROM logs WHERE {BY} = ? ORDER BY {sort_by} {'DESC' if descending else 'ASC'} LIMIT {limit} OFFSET {page * limit}''', (value,))
        else:
            return {
                "success": False,
                "message": "Invalid parameter",
                "body": None,
                "code": 400
            }
        column_names = [column[0] for column in cls.cursor.description]
        data = cls.cursor.fetchall()
        rows = []
        for row in data:
            rows.append(dict(zip(column_names, row)))
        return rows

    @classmethod
    def generate_error_codes(cls, length: int = 6, segments: int = 2, chars: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        """
        Generates a random cool looking error code like "ASRGFD-FEDCBA"
        Args:
            length (int): Length of each segment, default is 6.
            segments (int): Number of segments, default is 2.
            chars (str): Characters to be used, default is "ABCDEFGHIJKLMNOPQRSTUVWXYZ".
        """
        error_code = "-".join(["".join([random.choice(chars)
                              for i in range(length)]) for j in range(segments)])
        return error_code
