import pygame,sys

pygame.init()
pygame.mixer.init()

# General Settings
WIDTH, HEIGHT = 1080,720
TITLE = "Dating Sim"
FPS = 60
PLAYER_NAME = "DEFAULT"

TEXT_SCROLL_SPEED = 0.005 # in seconds
FADE_SPEED = 0.0001

# Credits
CREDITS = [
	"C R E D I T S",
	"",
	"Lead Programmer - Derek Zhang",
	"Code Assistant - Yi Deng",
	"Script - Stephen Hwang & Khushwant Virdi",
	"Original Art - Juleen Chen",
	"Music - Stephen Hwang",
	"Project Director - Stephen Hwang"
]

# Image Loading
def load(img):
	return pygame.image.load("../resources/images/"+img)

OPENING_BG = load("opening.png")
LOBBY_BG = load("backgrounds/lobby.png")
CLASSROOM_BG = load("backgrounds/classroom.png")
LOCKERS_BG = load("backgrounds/lockers.png")
PYTHON_BG = load("python.png")
SPLASH = load("splash.png")

EXPRESSIONS = [
	load("expressions/smile1.png"),load("expressions/smile2.png"),
	load("expressions/thinking.png"),load("expressions/sad.png"),
	load("expressions/weirded.png"),load("expressions/fbi.png"),
	load("expressions/embarressed.png")
]
BACKGROUNDS = [CLASSROOM_BG,LOCKERS_BG,LOBBY_BG,load("Backgrounds/51ending.png")]

# Font Definitions
comicsans50 = pygame.font.SysFont("comicsansms", 50)


# Music
MUSIC = [
"../resources/music/intro.mp3",
"../resources/music/bg_music.mp3",
"../resources/music/51_ending.mp3"
]

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
		if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
			return True
	return False

def set_player_name(name):
	global PLAYER_NAME
	PLAYER_NAME = name

