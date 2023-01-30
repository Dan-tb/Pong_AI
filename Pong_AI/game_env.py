import pygame


white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
blue1 = (0, 100, 255)
black = (0, 0, 0, 0)


class Ball:
    vel = 5

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.vel
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, white, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        # print(f'x = {self.x}, y = {self.y}')

    def ball_coordinates(self):
        self.x += self.x_vel
        self.y += self.y_vel
        return int(self.x), int(self.y)

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel = -1 * self.x_vel
        self.y_vel = 0


class Paddle:
    vel = 15
    color = white

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.w = width
        self.h = height

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))

    def _move(self, up=False, stationary=False, down=False):
        if stationary:
            self.y += 0

        if up:
            self.y -= self.vel

        if down:
            self.y += self.vel

    def paddle_coordinates(self):
        return self._move

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
