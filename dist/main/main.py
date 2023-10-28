from pong import Game
from pong import button
import pygame
import neat
import os
import pickle

class PongGame:
    width = 700
    height = 500

    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.leftPaddle = self.game.leftPaddle
        self.rightPaddle = self.game.rightPaddle
        self.ball = self.game.ball
    
    def testAi(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.movePaddle(left = True, up = True)
            if keys[pygame.K_s]:
                self.game.movePaddle(left = True, up = False)

            output = net.activate((self.rightPaddle.y, self.ball.y, abs(self.rightPaddle.x - self.ball.x)))
            decision = output.index(max(output))

            if decision == 0:
                pass
            elif decision == 1:
                self.game.movePaddle(left = False, up = True)
            else:
                self.game.movePaddle(left = False, up = False)


            gameInfo = self.game.loop()
            self.game.draw(True, False)
            pygame.display.update()

        pygame.quit()

    def trainAi(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()

            output1 = net1.activate((self.leftPaddle.y, self.ball.y, abs(self.leftPaddle.x - self.ball.x)))
            decision1 = output1.index(max(output1))

            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.game.movePaddle(left = True, up = True)
            else:
                self.game.movePaddle(left = True, up = False)

            output2 = net2.activate((self.rightPaddle.y, self.ball.y, abs(self.rightPaddle.x - self.ball.x)))
            decision2 = output2.index(max(output2))

            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.movePaddle(left = False, up = True)
            else:
                self.game.movePaddle(left = False, up = False)

            gameInfo = self.game.loop()
            self.game.draw(draw_score = False, draw_hits = True)
            pygame.display.update()

            if gameInfo.leftScore >= 1 or gameInfo.rightScore >= 1 or gameInfo.leftHits > 50:
                self.calcFitness(genome1, genome2, gameInfo)
                break
        
    def calcFitness(self, genome1, genome2, gameInfo):
        genome1.fitness += gameInfo.leftHits
        genome2.fitness += gameInfo.rightHits

def evalGenomes(genomes, config):
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = PongGame(window, width, height)
            game.trainAi(genome1, genome2, config)


def runNeat(config):
    pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-100')     #To restore back to a specified checkpoint
    # pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(1))

    winner = pop.run(evalGenomes, 1)
    with open("medium.pickle", "wb") as f:
              pickle.dump(winner, f)

def testAi(config, mode):
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))

    if mode == "EASY":
        with open("easy.pickle", "rb") as f:
            winner = pickle.load(f)
    elif mode == "MED":
        with open("medium.pickle", "rb") as f:
            winner = pickle.load(f)
    elif mode == "HARD":
        with open("hard.pickle", "rb") as f:
            winner = pickle.load(f)
    
    game = PongGame(window, width, height)
    game.testAi(winner, config)

def mainMenu():
    screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
    pygame.display.set_caption('PONG')

    player1_img = pygame.image.load(os.path.join("player1_btn.png")).convert_alpha()
    player2_img = pygame.image.load(os.path.join('player2_btn.png')).convert_alpha()

    player1Button = button.Button(700 / 4 - player1_img.get_width() // 2, 500 * (3/4) - (player1_img.get_height() // 2), player1_img, 1)
    player2Button = button.Button(700 * (3/4) - (player2_img.get_width() // 2), 500 * (3/4) - (player2_img.get_height() // 2), player2_img, 1)
    mainTitle = "PONG"
    text = Game.scoreFont.render(mainTitle, 1, Game.WHITE)

    run = True
    while run:

        screen.fill((33, 41, 48))
        screen.blit(text, (700 // 2 - (text.get_width() // 2), 500 * (1/4) - (text.get_height()) // 2))
        
        if player1Button.draw(screen):
            player1Screen()
        if player2Button.draw(screen):
            playPlayer2()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

def player1Screen ():
    screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))

    button_easy = pygame.image.load(os.path.join("button_easy.png")).convert_alpha()
    button_medium = pygame.image.load(os.path.join("button_medium.png")).convert_alpha()
    button_hard = pygame.image.load(os.path.join("button_hard.png")).convert_alpha()

    easyButton = button.Button(700 // 2 - (button_easy.get_width() // 2), 500 * (1/5) - (button_easy.get_height() // 2), button_easy, 1)
    medButton = button.Button(700 // 2 - (button_medium.get_width() // 2), 500 * (2/5) - (button_medium.get_height() // 2), button_medium, 1)
    hardButton = button.Button(700 // 2 - (button_hard.get_width() // 2), 500 * (3/5) - (button_hard.get_height() // 2), button_hard, 1)

    run = True
    while run:

        screen.fill((33, 41, 48))
        
        if easyButton.draw(screen):
            testAi(config, "EASY")
        if medButton.draw(screen):
            testAi(config, "MED")
        if hardButton.draw(screen):
            testAi(config, "HARD")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

def playPlayer2():
    window = pygame.display.set_mode((PongGame.width, PongGame.height))
    game = Game(window, PongGame.width, PongGame.height)

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
        game.draw(True, False)
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    localDir = os.path.dirname(__file__)
    configPath = os.path.join(localDir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         configPath)
    # runNeat(config)
    # testAi(config)

    mainMenu()