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
