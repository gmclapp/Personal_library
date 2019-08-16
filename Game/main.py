import pygame
import constants

class struct_tile():
    def __init__(self, tile_number):
        # Based on tile number get a tile definition to set its image and
        # whether it is blocking.
        # self.block_path = block_path

def map_create():
    new_map = [[struct_tile(False) for y in range(0,30)]for x in range(0,30)]
    new_map[10][10].block_path = True
    new_map[10][15].block_path = True
    return(new_map)
        
def quit_nicely():
    pygame.display.quit()
    pygame.quit()
    
def draw_game(SURFACE_MAIN):

    SURFACE_MAIN.fill(constants.DEFAULT_BG)

    # draw the scene

    # draw the character
    SURFACE_MAIN.blit(constants.S_PLAYER, (200,200))

    pygame.display.flip()

def game_main_loop(SURFACE_MAIN, game_map):
    game_quit = False
    fpsClock = pygame.time.Clock()
    
    while not game_quit:
        event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.QUIT:
                game_quit = True
        draw_game(SURFACE_MAIN)
        fpsClock.tick(60)

    quit_nicely()
                
def game_initialize():
    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH,
                                            constants.GAME_HEIGHT))
    game_map = map_create()

    return(SURFACE_MAIN, game_map)

if __name__ == "__main__":
    SURFACE_MAIN, game_map = game_initialize()
    game_main_loop(SURFACE_MAIN, game_map)
