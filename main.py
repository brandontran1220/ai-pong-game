from pong import Game
import pygame

class PongGame:
    width = 700
    height = 500

    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.leftPaddle = self.game.leftPaddle
        self.rightPaddle = self.game.rightPaddle
        self.ball = self.game.ball
    
    def testAi(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            game.handlePaddleMovement(keys)

            gameInfo = game.loop()
            print(gameInfo.leftScore, gameInfo.rightScore)
            game.draw(False, True)
            pygame.display.update()

        pygame.quit()
