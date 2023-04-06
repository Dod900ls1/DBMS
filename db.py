import sqlite3


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_database(self):
        query2 = """
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            model TEXT NOT NULL,
            memory TEXT NOT NULL,
            camera INTEGER NOT NULL
        )
        """

        self.cursor.execute(query2)
        self.conn.commit()
        print("Database created successfully.")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
                self.conn.commit()
            else:
                self.cursor.execute(query)
                self.conn.commit()
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def __del__(self):
        self.conn.close()
