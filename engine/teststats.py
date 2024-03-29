import random
import numpy as np
import string


def generate_test_stats():
    """
    Generates random test stats for the player prediction model.

    Format:
        data: [
            players: [
                name,
                round: [
                    kicks,
                    handballs,
                    marks,
                    tackles,
                    freekicksfor,
                    freekicksagainst,
                    hitouts,
                    goals,
                    behinds
                ]
            ]
        ]

    data = [[["name", None, None, None, None, None, None, None, None, None, None], ["cost", "kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds", "points"], ["kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds", "points"]], [["name", None, None, None, None, None, None, None, None], ["kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds", "points"], ["kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds", "points"]],[["name", None, None, None, None, None, None, None, None], ["kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds", "points"],["kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds", "points"]], [["name", None, None, None, None, None, None, None, None], ["kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds", "points"], ["kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds", "points"]]]
    """
    data = []
    for i in range(0, 1000):
        def create_rounds_year(year: int):
            round_num = {
                2020: 18,
                2021: 23,
                2022: 23,
                2023: 24
            }
            r_data = []
            for j in range(1, 25):
                if j > round_num[year]:
                    r_data.append([None, None, None, None, None,
                                  None, None, None, None, None, None, None])
                    continue
                round_id = f"{year}_R{j}"
                cost = random.randint(200000, 1100000)
                kicks = random.randint(0, 30)
                handballs = random.randint(0, 30)
                marks = random.randint(0, 30)
                tackles = random.randint(0, 30)
                freekicksfor = random.randint(0, 30)
                freekicksagainst = random.randint(0, 30)
                hitouts = random.randint(0, 30)
                goals = random.randint(0, 30)
                behinds = random.randint(0, 30)
                points = kicks*3 + handballs*2 + marks*3 + tackles*4 + \
                    freekicksfor - freekicksagainst*-3 + hitouts + goals*6 + behinds
                r_data.append([round_id, cost, kicks, handballs, marks, tackles,
                              freekicksfor, freekicksagainst, hitouts, goals, behinds, points])
            return r_data

        player_data = []
        player_data.append([f'{random.choice(string.ascii_uppercase)} {random.choice(string.ascii_uppercase)}'+''.join(
            random.choices(string.ascii_lowercase, k=10)), None, None, None, None, None, None, None, None, None, None, None])  # Name
        for j in range(0, 3):
            plh = [player_data.append(x) for x in create_rounds_year(2020+j)]
        data.append(player_data)
    return data


def generate_test_grounds():
    round_num = {
        2020: 18,
        2021: 23,
        2022: 23,
        2023: 24
    }
    afl_grounds = [
        "Melbourne Cricket Ground (MCG)",
        "Docklands Stadium",
        "The Gabba",
        "Adelaide Oval",
        "Perth Stadium",
        "Sydney Cricket Ground (SCG)",
        "Etihad Stadium (Marvel Stadium)",
        "Simonds Stadium",
        "The Western Oval"
    ]
    weathers = [
        "Sunny",
        "Rainy",
        "Windy",
        "Overcast",
        "Hail",
        "Snowy",
        "Foggy"
    ]
    grounds = []
    for year in range(2020, 2024):
        for i in range(1, 25):
            if i > round_num[year]:
                grounds.append([f"{year}_R{i}", None, None, None])
                continue
            round_id = f"{year}_R{i}"
            ground = random.choice(afl_grounds)
            temperature = random.randint(0, 40)
            weather = random.choice(weathers)
            grounds.append([round_id, ground, temperature, weather])
    return grounds


def generate_test_matches():
    round_num = {
        2020: 18,
        2021: 23,
        2022: 23,
        2023: 24
    }
    teams = [
        "Adelaide Crows",
        "Brisbane Lions",
        "Carlton Blues",
        "Collingwood Magpies",
        "Essendon Bombers",
        "Fremantle Dockers",
        "Geelong Cats",
        "Gold Coast Suns",
        "Greater Western Sydney Giants",
        "Hawthorn Hawks",
        "Melbourne Demons",
        "North Melbourne Kangaroos",
        "Port Adelaide Power",
        "Richmond Tigers",
        "St Kilda Saints",
        "Sydney Swans",
        "West Coast Eagles",
        "Western Bulldogs"
    ]
    matches = []
    for year in range(2020, 2024):
        for i in range(1, 25):
            if i > round_num[year]:
                matches.append(
                    [f"{year}_R{i}", None, None, None, None, None, None, None, None, None, None])
                continue
            round_id = f"{year}_R{i}"
            home_team = random.choice(teams)
            away_team = random.choice(teams)
            while away_team == home_team:
                away_team = random.choice(teams)
            date = f"{random.randint(1, 31)}/{random.randint(1, 12)}/{year}"
            time = f"{random.randint(0, 23)}:{random.randint(0, 59)}"
            matches.append([round_id, home_team, away_team,
                           date, time])
    return matches


if __name__ == "__main__":
    generate_test_stats()
