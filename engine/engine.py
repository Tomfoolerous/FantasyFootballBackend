import mysql.connector
import dotenv
import os
import requests
import numpy as np
import teststats
import player_predictions
import sys


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

    def _fetch_model_data(self) -> list:
        player_data = []
        ground_data = []
        if self.testing:
            player_data = teststats.generate_test_stats()
            player_data = [player[1:] for player in player_data]
            player_data = [[round[1:] for round in player]
                           for player in player_data]
            ground_data = teststats.generate_test_grounds()
            ground_data = [ground[1:] for ground in ground_data]
        return player_data, ground_data


if __name__ == "__main__":
    engine = Engine(testing=True)
    player_data, ground_data = engine._fetch_model_data()
    model = player_predictions.PredictedPlayerRatings()
    model.preprocess_data(player_data, ground_data)
    model.train_model()
    model.test_model()
    sys.exit()
