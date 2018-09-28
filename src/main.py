import pygame, math, random, sys
from pygame.locals import *
from settings import *
from classes import *

pygame.init()

class Game:
	def __init__(self):
		# initialize game window, etc
		pygame.init()
		pygame.mixer.init()
		pygame.display.init()
		pygame.display.set_caption(TITLE)

		self.window = pygame.display.set_mode((WIDTH,HEIGHT))
		self.clock = pygame.time.Clock()

		self.current_scene = Scene(exbg)
		self.current_scene.add_dialogue(Dialogue("How are you doing",[Response("well",2),Response("bad",3),Response("fuck u",4)]))
		self.player_choice = None

		self.game_state = "splash"

	def run(self):
		# Game Loop
		while 1:
			while self.game_state == "splash":
				for event in pygame.event.get():
					# check for closing window
					if event.type == pygame.QUIT:
						self.close()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE:
							self.game_state = "speaking"

				self.window.fill(BLACK)
				pygame.display.update()

			while self.game_state == "speaking":
				for event in pygame.event.get():
					# check for closing window
					if event.type == pygame.QUIT:
						self.close()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE:
							self.game_state = "replying"

				pygame.draw.rect(self.window, GREY, (200,510,WIDTH-400,150),5)
				self.current_scene.current_dialogue.play_text(self.window)

				pygame.display.update()
				self.clock.tick(FPS)

			while self.game_state == "replying":
				for event in pygame.event.get():
					# check for closing window
					if event.type == pygame.QUIT:
						self.close()
					if event.type == pygame.MOUSEBUTTONUP:
						if mx >= 200 and mx <= WIDTH-200:
							if my > 510 and my < 560:
								print(1)
							elif my > 560 and my < 610:
								print(2)
							elif my > 610 and my < 660:
								print(3)

				self.window.blit(self.current_scene.bg,(0,0))

				mx,my = pygame.mouse.get_pos()

				overlay = pygame.Surface((680,150));overlay.set_alpha(128);overlay.fill(BLACK)
				selector = pygame.Surface((680,50));selector.set_alpha(128);selector.fill(BLACK)

				self.window.blit(overlay,(200,510))

				if mx >= 200 and mx <= WIDTH-200:
					if my > 510 and my < 560:
						self.window.blit(selector,(200,510))
					elif my > 560 and my < 610:
						self.window.blit(selector,(200,560))
					elif my > 610 and my < 660:
						self.window.blit(selector,(200,610))

				'''pygame.draw.rect(self.window, BACK, (200,510,WIDTH-400,50),3)
				pygame.draw.rect(self.window, WHITE, (200,560,WIDTH-400,50),3)
				pygame.draw.rect(self.window, WHITE, (200,610,WIDTH-400,50),3)'''

				pygame.display.update()
				self.clock.tick(FPS)

	def text(self,text, font, size, color, x, y):
	    font_style = str(font)
	    font_size = size

	    text_font = pygame.font.SysFont(font_style, font_size)

	    message = text_font.render(text, True, color)

	    self.window.blit(message, (x, y))

	def close(self):
		pygame.quit()
		sys.exit()

if (__name__ == "__main__"):
	g = Game()
	g.run()

