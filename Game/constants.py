import pygame

pygame.init()

# Scene sizes are number of tiles in the scene.
SCENE_WIDTH_TILES = 24
SCENE_HEIGHT_TILES = 24

# Tile resolution
RES = 32

SCENE_WIDTH = SCENE_WIDTH_TILES * RES
SCENE_HEIGHT = SCENE_HEIGHT_TILES * RES

# Game sizes
GAME_WIDTH = SCENE_WIDTH + 256
GAME_HEIGHT = SCENE_HEIGHT + 224

# Color definitions
COLOR_BLACK = (0,0,0)
COLOR_GREY = (100,100,100)
COLOR_WHITE = (255,255,255)

# Game colors
DEFAULT_BG = COLOR_GREY
CHEAT_TXT = COLOR_WHITE
CHEAT_TXT_BOX_BG = COLOR_BLACK
DEBUG_TXT = COLOR_WHITE

# Sprites
S_PLAYER = pygame.image.load("data/character.png")

#Menus
MENU_FIRST_PAGE = pygame.image.load("data/Side bar menu first page.png")
MENU_MIDDLE_PAGE = pygame.image.load("data/Side bar menu middle page.png")
MENU_LAST_PAGE = pygame.image.load("data/Side bar menu last page.png")
