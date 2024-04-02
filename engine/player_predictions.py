import torch
import numpy as np
import pandas as pd
from torch.utils.tensorboard import SummaryWriter
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler

writer = SummaryWriter()


class PredictedPlayerRatings(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_stack = nn.Sequential(
            nn.Linear(1036, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
        )
        self.dataset = None

    def preprocess_data(self, player_data: np.array, ground_data: np.array):
        data = []
        # Normalise data
        for player in player_data:
            round_index = 0
            running_career_data = np.zeros((88, 11))
            running_five_match_data = np.zeros((5, 11))
            running_prev_match_data = np.zeros((1, 11))
            for index, round in enumerate(player):
                if None in player[index-1] or None in ground_data[round_index]:
                    continue
                if round != 0:
                    running_career_data[index-1] = player[index-1]
                    running_five_match_data[index %
                                            5] = player[index-1]
                    running_prev_match_data[0] = player[index-1]
                round_ground_data = ground_data[round_index]
                round_data = np.concatenate(
                    (running_career_data.flatten(), running_five_match_data.flatten(), running_prev_match_data.flatten(), round_ground_data))
                data.append(round_data)
                round_index += 1
        data = np.array(data, dtype=np.float32)
        data = StandardScaler().fit_transform(data)
        self.load_data(data)

    def load_data(self, data: np.array):
        def separate_data(data: np.array):
            np.random.shuffle(data)
            training, testing = np.array_split(data, 2)
            train_labels = training[:, 0]
            train_labels = train_labels.reshape(-1, 1)
            train_stats = training[:, 1:]
            test_labels = testing[:, 0]
            test_stats = testing[:, 1:]
            return train_labels, train_stats, test_labels, test_stats

        train_labels, train_stats, test_labels, test_stats = separate_data(
            data)
        self.dataset = TensorDataset(torch.tensor(
            train_stats, dtype=torch.float32), torch.tensor(train_labels, dtype=torch.float32))

    def _forward_propagation(self, x):
        logits = self.linear_stack(x)
        return logits

    def train_model(self):
        train_dataloader = DataLoader(
            self.dataset, batch_size=512, shuffle=True)
        loss_fn = nn.MSELoss()
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        for epoch in range(100):
            for stats, labels in train_dataloader:
                optimizer.zero_grad()
                pred = self._forward_propagation(stats)
                loss = loss_fn(pred, labels)
                loss.backward()
                optimizer.step()
            writer.add_scalar('Loss/train', loss, epoch)
            r_squared = 1 - loss / torch.var(labels)
            writer.add_scalar('R^2/train', r_squared, epoch)
            print(f'Epoch {epoch}: loss {loss.item()}')
        writer.flush()
        writer.close()

    def test_model(self):
        test_dataloader = DataLoader(
            self.dataset, batch_size=64, shuffle=True)
        loss_fn = nn.MSELoss()
        for stats, labels in test_dataloader:
            pred = self._forward_propagation(stats)
            loss = loss_fn(pred, labels)
            r_squared = 1 - loss / torch.var(labels)
            writer.add_scalar('Loss/test', loss, 0)
            writer.add_scalar('R^2/test', r_squared, 0)
            print(f'Test loss: {loss.item()}')
        writer.flush()
        writer.close()
