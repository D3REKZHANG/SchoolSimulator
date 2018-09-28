import pygame

class Player:
	def __init__(self,name):
		self.name = name
		self.score

class Dialogue:
	def __init__(self, text, responses):
		self.text = text
		self.responses = responses

	def play_text(self,window):
		pygame.draw.rect(window, (200,120,30), (100,100,200,200))

class Response:
	def __init__(self, text, target):
		self.text = text
		self.target_id = target

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
		self.current_dialogue = self.dialogues[self.current_dialogue.responses[option-1]]
