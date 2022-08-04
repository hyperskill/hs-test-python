import sqlite3


class SQLiteConnector:
    @staticmethod
    def connect(connection_params: dict[str, any]):
        database = ':memory:'
        if 'database' in connection_params:
            database = connection_params['database']

        try:
            return sqlite3.connect(database, **connection_params)
        except sqlite3.Error:
            raise Exception(f"Can't connect to the SQLite database with the following parameters:\n"
                            f"{connection_params}")
