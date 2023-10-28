import pygame
import button
import os

pygame.init()

WIDTH, HEIGHT = 700, 500
scoreFont = pygame.font.SysFont("impact", 100)
WHITE = (255, 255, 255)

def mainMenu():
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Main Menu')

	player1_img = pygame.image.load(os.path.join("player1_btn.png")).convert_alpha()
	player2_img = pygame.image.load(os.path.join('player2_btn.png')).convert_alpha()

	player1Button = button.Button(WIDTH / 4 - player1_img.get_width() // 2, HEIGHT * (3/4) - (player1_img.get_height() // 2), player1_img, 1)
	player2Button = button.Button(WIDTH * (3/4) - (player2_img.get_width() // 2), HEIGHT * (3/4) - (player2_img.get_height() // 2), player2_img, 1)
	mainTitle = "PONG"
	text = scoreFont.render(mainTitle, 1, WHITE)

	run = True
	while run:

		screen.fill((33, 41, 48))
		screen.blit(text, (WIDTH // 2 - (text.get_width() // 2), HEIGHT * (1/4) - (text.get_height()) // 2))
		
		if player1Button.draw(screen):
			print('START')
		if player2Button.draw(screen):
			print('EXIT')

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		pygame.display.update()

	pygame.quit()