import pygame

class Paddle:
    VEL = 4
    WIDTH, HEIGHT = 20, 100

    def __init__(self, x, y, color):
        self.x = self.originalX = x
        self.y = self.originalY = y
        self.COLOR = color

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.WIDTH, self.HEIGHT))    
    
    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.originalX
        self.y = self.originalY