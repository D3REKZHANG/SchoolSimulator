import pygame

pygame.init()

# General Settings
WIDTH, HEIGHT = 1080,720
TITLE = "Dating Sim"
FPS = 60

# Image Loading
path = "../resources/images/"
exbg = pygame.image.load("{}example_bg.jpg".format(path))

# Colour Definitions
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN= (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
AQUA = (0,255,255)
GREY = (200,200,200)
