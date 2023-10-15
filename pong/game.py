from .paddle import Paddle
from .ball import Ball
import pygame
import random
pygame.init()

class GameInformation:
    def __init__(self, leftHits, rightHits, leftScore, rightScore):
        self.leftHits = leftHits
        self.rightHits = rightHits
        self.leftScore = leftScore
        self.rightScore = rightScore

class Game:
    WIDTH, HEIGHT = 700, 500
    scoreFont = pygame.font.SysFont("impact", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0 , 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    def __init__(self, window, windowWidth, windowHeight):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        self.leftPaddle = Paddle(10, self.windowHeight // 2 - Paddle.HEIGHT // 2, Game.RED)
        self.rightPaddle = Paddle(self.windowWidth - 10 - Paddle.WIDTH , self.windowHeight // 2 - Paddle.HEIGHT // 2, Game.BLUE)
        self.ball = Ball(self.windowWidth // 2, self.windowHeight // 2)

        self.leftScore = 0
        self.rightScore = 0
        self.leftHits = 0
        self.rightHits = 0
        self.window = window

    def drawScore(self):        
        leftScore_text = Game.scoreFont.render(f"{self.leftScore}", 1, Game.RED)
        rightScore_text = Game.scoreFont.render(f"{self.rightScore}", 1, Game.BLUE)
        self.window.blit(leftScore_text, (self.windowWidth // 4 - leftScore_text.get_width() // 2, 20))
        self.window.blit(rightScore_text, (self.windowWidth * (3/4) - rightScore_text.get_width() // 2, 20))
    
    def drawHits(self):
        hitsText = self.scoreFont.render(f"{self.leftHits + self.rightHits}", 1, self.RED)
        self.window.blit(hitsText, (self.windowWidth // 2 - hitsText.get_width()//2, 10))
    
    def drawDivider(self):
        for i in range(10, self.windowHeight, self.windowHeight // 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(self.window, self.WHITE, (self.windowWidth // 2 - 5, i, 10, self.windowHeight // 20))

    def handleCollision(self):
        ball = self.ball
        leftPaddle = self.leftPaddle
        rightPaddle = self.rightPaddle

        if ball.y + Ball.RADIUS >= self.windowHeight:
            ball.yVel *= -1
        elif ball.y - Ball.RADIUS <= 0:
            ball.yVel *= -1

        if ball.xVel < 0:
            if ball.y >= leftPaddle.y and ball.y <= leftPaddle.y + Paddle.HEIGHT:
                if ball.x - Ball.RADIUS <= leftPaddle.x + Paddle.WIDTH:
                    self.leftHits += 1
                    ball.xVel *= -1

                    middle_y = leftPaddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MaxVel
                    yVel = difference_in_y / reduction_factor
                    ball.yVel = -1 * yVel

        else:
            if ball.y >= rightPaddle.y and ball.y <= rightPaddle.y + Paddle.HEIGHT:
                if ball.x + Ball.RADIUS >= rightPaddle.x:
                    self.rightHits += 1
                    ball.xVel *= -1

                    middle_y = rightPaddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MaxVel
                    yVel = difference_in_y / reduction_factor
                    ball.yVel = -1 * yVel

    def reset(self):
        self.ball.reset()
        self.leftPaddle.reset()
        self.rightPaddle.reset()
        self.leftScore = 0
        self.rightScore = 0
        self.leftHits = 0
        self.rightHits = 0

    def draw(self, draw_score = True, draw_hits = False):
        self.window.fill(self.BLACK)
        self.drawDivider()

        if draw_score:
            self.drawScore()
        
        if draw_hits:
            self.drawHits()

        for paddle in [self.leftPaddle, self.rightPaddle]:
            paddle.draw(self.window)
        
        self.ball.draw(self.window)

    def handlePaddleMovement(self, keys):
        if keys[pygame.K_w] and self.leftPaddle.y - Paddle.VEL >= 0:
            self.leftPaddle.move(up=True)
        if keys[pygame.K_s] and self.leftPaddle.y + Paddle.VEL + Paddle.HEIGHT <= self.windowHeight:
            self.leftPaddle.move(up=False)

        if keys[pygame.K_UP] and self.rightPaddle.y - Paddle.VEL >= 0:
            self.rightPaddle.move(up=True)
        if keys[pygame.K_DOWN] and self.rightPaddle.y + Paddle.VEL + Paddle.HEIGHT <= self.windowHeight:
            self.rightPaddle.move(up=False)

    def loop(self):
        self.ball.move()
        self.handleCollision()

        if self.ball.x < 0:
            self.ball.reset()
            self.rightScore += 1
        elif self.ball.x > self.windowWidth:
            self.ball.reset()
            self.leftScore += 1
        
        gameInfo = GameInformation(self.leftHits, self.rightHits, self.leftScore, self.rightScore)

        return gameInfo