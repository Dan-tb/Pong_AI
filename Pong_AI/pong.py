import pygame
from game_env import Ball, Paddle
import numpy as np

# initialise the pygame environment
pygame.init()

# setting the size of the game environment
height = 480
width = 800

# setting the size of the paddle
paddle_width = 20
paddle_height = 100

game_score_font = pygame.font.SysFont("comicsans", 50)

white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
blue1 = (0, 100, 255)
black = (0, 0, 0, 0)

# initialising the paddle and ball class
right_paddle = Paddle(
    (width - 20 - paddle_width),
    (height // 2 - paddle_height // 2),
    paddle_width,
    paddle_height,
)
# creating instance of the Ball
ball = Ball(width // 2, height // 2, 10)


# creating the pong class
class PingpongAI:
    def __init__(self, width=800, height=480):
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((self.width, self.height))
        self.score = 0
        self.reset()
        pygame.display.set_caption("ping pong")

    # draw the ball, paddle, display text, and update the screen
    def _draw(self):
        self.win.fill(black)
        ball.draw(self.win)
        right_paddle.draw(self.win)
        left_text = game_score_font.render(f"{self.score}", 1, white)
        self.win.blit(left_text, (width * 3 // 4 - left_text.get_width() // 2, 20))
        pygame.display.update()

    # handle the movement of the paddle either up, down
    def _handle_paddle_movement(self, action):
        # movement = random.randint(0,2)

        # moving the paddle up
        if np.array_equal(action, [0, 1, 0]) and right_paddle.y - right_paddle.vel >= 0:
            right_paddle._move(up=True)

        # moving the paddle down
        if (
            np.array_equal(action, [0, 0, 1])
            and right_paddle.y + right_paddle.vel + right_paddle.h <= height
        ):
            right_paddle._move(down=True)

        # making the paddle stationary
        if (
            np.array_equal(action, [1, 0, 0])
            and right_paddle.y + right_paddle.vel + right_paddle.h <= height
            and right_paddle.y - right_paddle.vel >= 0
        ):
            right_paddle._move(stationary=True)

    # handle the collisions between the ball, paddle and environment
    def _handle_collisions(self, ball, right_paddle):
        # collision of the ball on the top
        if ball.y + ball.radius >= self.height:
            ball.y_vel *= -1

            return True

        # collision on the bottom
        elif ball.y - ball.radius <= 0:
            ball.y_vel *= -1

            return True

        if ball.x_vel > 0:
            # collision of the ball on the paddle
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.h:
                if ball.x + ball.radius >= right_paddle.x:
                    ball.x_vel *= -1

                    middle_y = right_paddle.y + right_paddle.h / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (right_paddle.h / 2) / right_paddle.vel
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel

                    return True

        else:
            if ball.x + ball.radius < 19:
                ball.x_vel *= -1

                return True

        return False

    # reset the game environment
    def reset(self):
        pygame.display.update()
        pygame.time.delay(1000)
        ball.reset()
        right_paddle.reset()
        self.score = 0

    # play the game
    def step(self, action_taken):
        # increasing the speed of the game
        clock = pygame.time.Clock()
        clock.tick(40)

        self._draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()

        self._handle_paddle_movement(action_taken)
        ball.move()
        self._handle_collisions(ball, right_paddle)
        reward = 0

        # check win status by inplementing a winning criteria
        game_over = False
        if self.score >= 20:
            reward = -20
            game_over = True
            self.reset()

            # return reward, game_over, self.score

        if ball.x > self.width:
            reward = -10
            self.score += 1
            ball.reset()
            right_paddle.reset()

        return reward, game_over, self.score


# ping = PingpongAI()
# while True:
#     reward, game_over, score = ping.step()
#     print(f"reward  {reward}\n game_over {game_over}\n score  {score}")
