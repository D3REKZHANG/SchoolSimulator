import pygame,sys

pygame.init()

# General Settings
WIDTH, HEIGHT = 1080,720
TITLE = "Dating Sim"
FPS = 60
PLAYER_NAME = "DEFAULT"

TEXT_SCROLL_SPEED = 0.005 # in seconds
FADE_SPEED = 0.0001

# Image Loading
path = "../resources/images/"
exbg = pygame.image.load("{}example_bg.jpg".format(path))
exbg2 = pygame.image.load("{}example_bg2.jpg".format(path))
exbg3 = pygame.image.load("{}example_bg3.jpg".format(path))
OPENING_BG = pygame.image.load("{}opening.jpg".format(path))

BACKGROUNDS = [exbg,exbg2,exbg3]

exchar = pygame.image.load("{}talking.png".format(path))

# Font Definitions
comicsans50 = pygame.font.SysFont("comicsansms", 50)

# Colour Definitions
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN= (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
AQUA = (0,255,255)
GREY = (200,200,200)

# Fancy Functions
def find_space_backwards(string, index):
	for i in range(index,0,-1):
		if string[i] == ' ':
			return i

def check_break():
	for event in pygame.event.get():
		# check for closing window
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				return True
	return False

def set_player_name(name):
	global PLAYER_NAME
	PLAYER_NAME = name