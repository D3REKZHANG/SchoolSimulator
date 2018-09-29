import pygame,time
from settings import *

class Player:
	def __init__(self,name):
		self.name = name
		self.score

class Dialogue:
	def __init__(self, text, responses, image):
		self.t = text
		self.responses = responses
		self.image = image

	def play_text(self,window,bg,overlay,x,y):
		text_font = pygame.font.SysFont("arial", 25)
		message = text_font.render(self.t, True, WHITE)

		if message.get_width() > WIDTH-410:
			#split the message into sections
			index = int(len(self.t)*(WIDTH-410)/(message.get_width()))
			t1 = self.t[:find_space_backwards(self.t,index)]

			if(message.get_width()/(WIDTH-410))>2:
				index2 = int((len(self.t)-index)*(WIDTH-410)/(message.get_width()))
				t2 = self.t[find_space_backwards(self.t,index):find_space_backwards(self.t,index2)].strip()
				t3 = self.t[find_space_backwards(self.t,index2):].strip()
			else:
				t2 = self.t[find_space_backwards(self.t,index):].strip()

			for i in range(len(t1)):
				if check_break():
					break
				window.blit(bg,(0,0))
				window.blit(overlay,(200,510))
				window.blit(self.image,(0,0))
				self.text(window, t1[:i],"arial", 25, WHITE, x, y)
				time.sleep(TEXT_SCROLL_SPEED)
				pygame.display.update()
			for i in range(len(t2)):
				if check_break():
					break
				window.blit(bg,(0,0))
				window.blit(overlay,(200,510))
				window.blit(self.image,(0,0))
				self.text(window, t1,"arial",25,WHITE,x,y)
				self.text(window, t2[:i],"arial", 25, WHITE, x, y+30)
				time.sleep(TEXT_SCROLL_SPEED)
				pygame.display.update()
			if(message.get_width()/(WIDTH-400)>2):
				for i in range(len(t3)):
					if check_break():
						break
					window.blit(bg,(0,0))
					window.blit(overlay,(200,510))
					window.blit(self.image,(0,0))
					self.text(window, t1,"arial",25,WHITE,x,y)
					self.text(window, t2,"arial", 25, WHITE, x, y+30)
					self.text(window, t3[:i],"arial", 25, WHITE, x, y+60)

					time.sleep(TEXT_SCROLL_SPEED)
					pygame.display.update()
		else:
			for i in range(len(self.t)):
				if check_break():
					break
				window.blit(bg,(0,0))
				window.blit(overlay,(200,510))
				window.blit(self.image,(0,0))
				self.text(window, self.t[:i],"arial", 25, WHITE, x, y)
				time.sleep(TEXT_SCROLL_SPEED)
				pygame.display.update()

	def text(self, window, text, font, size, color, x, y):
		font_style = str(font)
		font_size = size

		text_font = pygame.font.SysFont(font_style, font_size)
		message = text_font.render(text, True, color)
		
		window.blit(message, (x, y))

class Response:
	def __init__(self, text, target,scene_change = False):
		self.text = text
		self.target_id = target
		self.scene_change = scene_change

class Scene:
	def __init__(self,bg):
		self.bg = bg
		self.dialogues = []
		self.current_dialogue = None
		self.fresh = True

	def add_dialogue(self,dial):		
		self.dialogues.append(dial)
		if self.fresh:
			self.current_dialogue = self.dialogues[0]
			self.fresh = False

	def input(self, option):
		''' option -> response 1, 2, or 3'''
		self.current_dialogue = self.dialogues[self.current_dialogue.responses[option-1].target_id]
