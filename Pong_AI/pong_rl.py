# importing necessary libraries
from Agent import Agent
from pong import PingpongAI
import time


# creating instance of game and agent
game = PingpongAI()
agent = Agent()

best_time_alive = 0
while True:
    clock = time.time()
    # get the current state of the environment
    state = agent.get_state(game)
    # take an action based on the state
    action = agent.get_action(state)
    # get the reward, gameover and current score
    reward, game_over, score = game.step(action)
    # get the next_state of the environment after taking action
    next_state = agent.get_state(game)
    # train the immediate state,action, reward, next_state, game_over
    agent.train_short_memory(state, action, reward, next_state, game_over)
    # store the trained data
    agent.remember(state, action, reward, next_state, game_over)

    if game_over:
        clock2 = time.time()
        # refresh game
        game.reset()
        # refresh counter
        agent.games += 1
        # train on variety of generated data
        agent.train_long_memory()

        time_alive = clock2 - clock

        if time_alive > best_time_alive:
            best_time_alive = time_alive
            # print(best_time_alive)
            agent.model.save_model()
