# import libraries
from torch import nn
import torch
import os

# neural network class
class Q_net(nn.Module):
    def __init__(self, input, hidden_size, output):
        super(Q_net, self).__init__()
        self.linear_net = nn.Sequential(
            nn.Linear(input, hidden_size), nn.ReLU(), nn.Linear(hidden_size, output)
        )

    def forward(self, x):
        x = self.linear_net(x)
        return x

    def save_model(self, filename="model.pth"):
        path_file = "./models"
        if not os.path.exists(path_file):
            os.makedirs(path_file)

        file_name = os.path.join(path_file, filename)
        torch.save(self.state_dict(), file_name)


class Q_learner:
    def __init__(self, model, learning_rate, gamma):
        self.model = model
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.optimizer = torch.optim.Adam(self.model.parameters(), self.learning_rate)
        self.criterion = nn.MSELoss()

    def train(self, state, action, reward, next_state, done):
        # defining the state, action, reward, next_state tensors
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            next_state = torch.unsqueeze(next_state, 0)
            done = (done,)

        pred = self.model(state)
        target = pred.clone()

        for idx in range(len(done)):
            # initialising the Q_value_network
            Q_new = reward[idx]
            if not done[idx]:
                # the bellman equation of the Q_network
                Q_new = reward[idx] + self.gamma * torch.max(
                    self.model(next_state[idx])
                )

            # getting the index value of action too
            target[idx][torch.argmax(action).item()] = Q_new

        # backpropagation algorithm
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()
