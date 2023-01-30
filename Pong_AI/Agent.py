from collections import deque
from pong import right_paddle, ball
from collections import namedtuple
from model import Q_learner, Q_net
import numpy as np
import random
import torch

REPLAY_BUFFER_SIZE = 200000
REPLAY_BUFFER_BATCH_SIZE = 1000
# EPSILON_DECAY = [0.99910, 0.99941, 0.99954, 0.99973, 0.99987]
LEARNING_RATE = 0.0001
GAMMA = 0.9

Point = namedtuple("Point", "x, y")

width = 800
height = 480

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device.....")


class Agent:
    def __init__(self):
        self.games = 0
        self.model = Q_net(7, 256, 3).to(device=device)
        self.learning_rate = LEARNING_RATE
        self.gamma = GAMMA
        # self.epsilon_decay = EPSILON_DECAY[1]
        self.epsilon = 0
        self.memory = deque(maxlen=REPLAY_BUFFER_SIZE)
        self.learner = Q_learner(self.model, self.learning_rate, self.gamma)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_short_memory(self, state, action, reward, next_state, done):
        self.learner.train(state, action, reward, next_state, done)

    def train_long_memory(self):
        if len(self.memory) > REPLAY_BUFFER_BATCH_SIZE:
            mini_sample = random.sample(self.memory, REPLAY_BUFFER_BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, done = zip(*mini_sample)
        self.learner.train(states, actions, rewards, next_states, done)

    def get_action(self, state):
        final_move = [0, 0, 0]
        explore = 100 - self.games
        if random.randint(0, 200) < explore:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state_init = torch.tensor(state, dtype=torch.float)
            pred = self.model(state_init)
            action = torch.argmax(pred).item()
            final_move[action] = 1

        return final_move

    def get_state(self, game):
        # the agent current location i.e the paddle
        locate_y = right_paddle.paddle_coordinates
        paddle_location = Point(right_paddle.x, locate_y)

        # the ball current location
        locate_1, locate_2 = ball.ball_coordinates()
        ball_location = Point(locate_1, locate_2)

        # collision of the ball on the paddle and other part of the environment
        state = [
            (ball_location.x == range(0, width)),
            (ball_location.y == range(0, height)),
            (paddle_location.y == range(0, height)),
            (ball.x_vel > 0 and game._handle_collisions(ball, right_paddle)),
            (
                ball.y + ball.radius >= height
                and game._handle_collisions(ball, right_paddle)
            ),
            (ball.y - ball.radius <= 0 and game._handle_collisions(ball, right_paddle)),
            (ball.x_vel > 0 and game._handle_collisions(ball, right_paddle)),
        ]

        return np.array(state, dtype=int)
