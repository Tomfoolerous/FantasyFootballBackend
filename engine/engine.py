import mysql.connector
import dotenv
import os
import requests
import numpy as np
import teststats


class Engine:
    def __init__(self, testing=False):
        dotenv.load_dotenv()
        self.testing = testing

        if not self.testing:
            self.conn = mysql.connector.connect(
                host="localhost",
                password=os.getenv("DB_PASSWORD"),
                user=os.getenv("DB_USER"),
                database=os.getenv("DB_NAME")
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            self._initialise_db()

        self.session = requests.Session()
        self.session.headers.update(
            
            {"User-Agent": f"FantasyFootballBackend - Contact at {os.getenv('EMAIL')}"})

        self._fetch_model_data()

        self.fetch_model_data()

    def _run_sql(self, sql, values) -> tuple:
        self.cursor.execute(sql, values)
        return self.cursor.fetchall()

    def _initialise_db(self) -> bool:
        self._run_sql("CREATE DATABASE IF NOT EXISTS %s",
                      (os.getenv("DB_NAME"),))
        self._run_sql("USE %s", (os.getenv("DB_NAME"),))
        for i in range(0, 5):
            self._run_sql(
                f"CREATE TABLE IF NOT EXISTS players_202{i} (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name TEXT, cost INT, kicks INT, handballs INT, marks INT, tackles INT, freekicksfor INT, freekicksagainst INT, hitouts INT, goals INT, behinds INT, team TEXT)", ())
            self._run_sql(
                f"CREATE TABLE IF NOT EXISTS matches_202{i} (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, home_team TEXT, away_team TEXT, ground_id INT, date DATE, time TIME, home_points INT, away_points INT, temperature INT, weather TEXT)", ())
        self._run_sql(
            "CREATE TABLE IF NOT EXISTS teams (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name TEXT, colour TEXT, coach TEXT)", ())
        self._run_sql(
            "CREATE TABLE IF NOT EXISTS grounds (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name TEXT, capacity INT)", ())
        return True

    def _numerify_list(self, data: list) -> np.array:
        # Converts all the strings into integers for processing.
        # Byte conversion used to increase performance (operations run at C speed).
        def convert_value(value: str):
            if isinstance(value, int):
                return value
            b_value = value.encode("utf-8")
            i_value = int.from_bytes(b_value, "big")
            return i_value

        return np.vectorize(convert_value)(data)

    def _fetch_model_data(self) -> np.array:
        years = range(2020, 2025)
        rounds = range(1, 24)
        rounds_2020 = range(1, 18)
        player_data = []
        ground_data = []
        match_data = []
        for year in years:
            for round in rounds_2020 if year == 2020 else rounds:
                if self.testing:
                    player_data = teststats.generate_test_stats()
                    ground_data = teststats.generate_test_grounds()
                    match_data = teststats.generate_test_matches()
                    continue
                pass
        r_player_data = self._numerify_list(player_data)
        r_ground_data = self._numerify_list(ground_data)
        r_match_data = self._numerify_list(match_data)
        return r_player_data, r_ground_data, r_match_data
