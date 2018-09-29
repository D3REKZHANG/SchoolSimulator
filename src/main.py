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
		self.current_scene.add_dialogue(Dialogue("D0",[Response("z",1),Response("z",1),Response("z",1)],exchar))
		self.current_scene.add_dialogue(Dialogue("RANDOM GIRL: Hi! I haven't seen you around ... nice to meet you!",[Response("Likewise! What's your name?",2),Response("Ew, get away from me",3),Response("Gtfo cuz u know u a thot",4)],exchar))
		self.current_scene.add_dialogue(Dialogue("D2",[Response("3",3),Response("4",4),Response("1",1)],exchar))
		self.current_scene.add_dialogue(Dialogue("D3",[Response("4",4),Response("1",1),Response("2",2)],exchar))
		self.current_scene.add_dialogue(Dialogue("D4",[Response("1",1),Response("2",2),Response("3",3)],exchar))

		self.game_state = "splash"

		self.text_anim = True

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
				self.text("S P L A S H S C R E E N", "Courier New",30,WHITE,0,0,align="center")
				pygame.display.update()

			while self.game_state == "speaking":
				for event in pygame.event.get():
					# check for closing window
					if event.type == pygame.QUIT:
						self.close()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE:
							self.game_state = "replying"

				if self.game_state != "speaking":
					break

				self.window.blit(self.current_scene.bg,(0,0))

				# Draw Character
				self.window.blit(self.current_scene.current_dialogue.image,(0,0))

				overlay = pygame.Surface((680,150));overlay.set_alpha(128);overlay.fill(BLACK)
				self.window.blit(overlay,(200,510))

				if self.text_anim:
					self.current_scene.current_dialogue.play_text(self.window,self.current_scene.bg,overlay,210,520)
					self.text_anim = False
				else:
					tt = self.current_scene.current_dialogue.t
					text_font = pygame.font.SysFont("arial", 25)
					message = text_font.render(tt, True, WHITE)

					if message.get_width() > WIDTH-410:
						#split the message into sections 
						index = int(len(tt)*(WIDTH-410)/(message.get_width()))
						t1 = tt[:find_space_backwards(tt,index)]
						t2 = tt[find_space_backwards(tt,index):]
						self.text(t1,"arial",25,WHITE,210,520)
						self.text(t2.strip(),"arial",25,WHITE,210,550)
					else:
						self.text(tt,"arial",25,WHITE,210,520)

				pygame.display.update()
				self.clock.tick(FPS)

			while self.game_state == "replying":
				for event in pygame.event.get():
					# check for closing window
					if event.type == pygame.QUIT:
						self.close()
					if event.type == pygame.MOUSEBUTTONUP:
						# Check for button clicks
						if mx >= 200 and mx <= WIDTH-200:
							if my > 510 and my < 660:
								if my > 510 and my < 560:
									print(1)
									self.current_scene.input(1)
								elif my > 560 and my < 610:
									self.current_scene.input(2)
								elif my > 610 and my < 660:
									self.current_scene.input(3)
								self.text_anim = True
								self.game_state = "speaking"

				if self.game_state != "replying":
					break

				# Clear screen
				self.window.blit(self.current_scene.bg,(0,0))

				# Draw Character
				self.window.blit(self.current_scene.current_dialogue.image,(0,0))

				# Grab mouse position
				mx,my = pygame.mouse.get_pos()

				# Declaring the faded overlay and selector
				overlay = pygame.Surface((680,150));overlay.set_alpha(128);overlay.fill(BLACK)
				selector = pygame.Surface((680,50));selector.set_alpha(128);selector.fill(BLACK)

				# Overlay Render
				self.window.blit(overlay,(200,510))

				# Selector Render
				if mx >= 200 and mx <= WIDTH-200:
					if my > 510 and my < 560:
						self.window.blit(selector,(200,510))
					elif my > 560 and my < 610:
						self.window.blit(selector,(200,560))
					elif my > 610 and my < 660:
						self.window.blit(selector,(200,610))

				# Actual Replies
				for i in range(3): 
					t = self.current_scene.current_dialogue.responses[i].text
					
					self.text(t, "arial", 25, WHITE, 210, 518+50*i)


				pygame.display.update()
				self.clock.tick(FPS)

	def text(self,text, font, size, color, x, y, align="free"):
	    font_style = str(font)
	    font_size = size

	    text_font = pygame.font.SysFont(font_style, font_size)

	    message = text_font.render(text, True, color)
	    if(align == "center"):
	    	self.window.blit(message, (WIDTH/2-message.get_width()//2, HEIGHT/2-message.get_height()//2))
	    else:
	    	self.window.blit(message, (x, y))

	def close(self):
		pygame.quit()
		sys.exit()

if (__name__ == "__main__"):
	g = Game()
	g.run()

