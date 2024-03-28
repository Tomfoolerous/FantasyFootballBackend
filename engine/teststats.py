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

    data = [[["name", None, None, None, None, None, None, None, None], ["cost", "kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds"], ["kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds"]], [["name", None, None, None, None, None, None, None, None], ["kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds"], ["kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds"]],[["name", None, None, None, None, None, None, None, None], ["kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds"],["kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds"]], [["name", None, None, None, None, None, None, None, None], ["kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds"], ["kicks", "handballs", "marks", "tackles", "freekicksfor", "freekicksagainst", "hitouts", "goals", "behinds"]]]
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
            for j in range(1, round_num[year]):
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
                r_data.append([round_id, cost, kicks, handballs, marks, tackles, freekicksfor, freekicksagainst, hitouts, goals, behinds])
            return r_data
        
        player_data = []
        player_data.append([f'{random.choice(string.ascii_uppercase)} {random.choice(string.ascii_uppercase)}'+''.join(random.choices(string.ascii_lowercase, k=10)), None, None, None, None, None, None, None, None]) # Name
        for j in range(0, 3):
            player_data.append(create_rounds_year(int(f"202{j}")))
        data.append(player_data)
    print(data[0])
    return data

generate_test_stats()