import mysql.connector
import dotenv
import os


class Engine:
    def __init__(self):
        dotenv.load_dotenv()
        self.conn = mysql.connector.connect(
            host="localhost",
            password=os.getenv("DB_PASSWORD"),
            user=os.getenv("DB_USER"),
            database=os.getenv("DB_NAME")
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def _run_sql(self, sql, values):
        self.cursor.execute(sql, values)
        return self.cursor.fetchall()
