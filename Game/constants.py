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

# Sprites
S_PLAYER = pygame.image.load("data/character.png")

# Tiles
CAVE_WALL = pygame.image.load("data/cave_wall.png")
CAVE_FLOOR = pygame.image.load("data/cave_floor.png")
