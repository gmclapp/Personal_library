import pygame

pygame.init()

# Game sizes
GAME_WIDTH = 800
GAME_HEIGHT = 600

# Scene sizes are number of tiles in the scene.
SCENE_WIDTH_TILES = 15
SCENE_HEIGHT_TILES = 15

# Tile resolution
RES = 64

SCENE_WIDTH = SCENE_WIDTH_TILES * RES
SCENE_HEIGHT = SCENE_HEIGHT_TILES * RES

# Color definitions
COLOR_BLACK = (0,0,0)
COLOR_GREY = (100,100,100)

# Game colors
DEFAULT_BG = COLOR_GREY

# Sprites
S_PLAYER = pygame.image.load("data/character.png")

# Tiles
CAVE_WALL = pygame.image.load("data/cave_wall.png")
CAVE_FLOOR = pygame.image.load("data/cave_floor.png")
