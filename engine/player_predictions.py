import torch
import numpy as np
import pandas as pd
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


class PredictedPlayerRatings:
    def __init__(self):
        self.dataset = None

    def load_data(self, data: np.array):
        """
        Ideal data provided:
            career_data = [career_kicks, career_handballs, career_marks, career_tackles, career_freekicksfor, career_freekicksagainst, career_hitouts, career_goals, career_behinds]
            five_match_data = [five_match_kicks, five_match_handballs, five_match_marks, five_match_tackles, five_match_freekicksfor, five_match_freekicksagainst, five_match_hitouts, five_match_goals, five_match_behinds]
            prev_match_data = [prev_match_kicks, prev_match_handballs, prev_match_marks, prev_match_tackles, prev_match_freekicksfor, prev_match_freekicksagainst, prev_match_hitouts, prev_match_goals, prev_match_behinds]
            ground_data = [ground_id, temperature, weather]
            match_data = [home_team, away_team, date, time]
        """

        def separate_data(data: np.array):
            s_data = np.random.shuffle(data)
            training, testing = np.array_split(s_data, 2)
            train_labels = training[:, 0]
            train_stats = training[:, 1:]
            test_labels = testing[:, 0]
            test_stats = testing[:, 1:]
            return train_labels, train_stats, test_labels, test_stats

        train_labels, train_stats, test_labels, test_stats = separate_data(
            data)

        self.dataset = TensorDataset(torch.tensor(
            train_stats, dtype=torch.float32), torch.tensor(train_labels, dtype=torch.float32))
