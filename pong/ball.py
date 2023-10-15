import pygame
import math
import random

class Ball:
    RADIUS = 7
    MaxVel = 7
    WHITE = (255, 255, 255)

    def __init__(self, x, y):
        self.x = self.originalX = x
        self.y = self.originalY = y
        
        angle = self.getRandomAngle(-30, 30, [0])
        pos = 1 if random.random() < 0.5 else -1

        self.xVel = pos * abs(math.cos(angle) * self.MaxVel)
        self.yVel = math.sin(angle) * self.MaxVel

    def draw(self, win):
        pygame.draw.circle(win, self.WHITE, (self.x, self.y), Ball.RADIUS)

    def move(self):
        self.x += self.xVel
        self.y += self.yVel

    def reset(self):
        self.x = self.originalX
        self.y = self.originalY
        
        newAngle = self.getRandomAngle(-30, 30, [0])
        xVel = abs(math.cos(newAngle) * self.MaxVel)
        yVel = math.sin(newAngle) * self.MaxVel

        self.yVel = yVel
        self.xVel *= -1
    
    def getRandomAngle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))
        
        return angle
    
