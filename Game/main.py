import pygame
import constants

def quit_nicely():
    pygame.display.quit()
    pygame.quit()
    
def draw_game(SURFACE_MAIN):

    SURFACE_MAIN.fill(constants.DEFAULT_BG)

    # draw the scene

    # draw the character
    SURFACE_MAIN.blit(constants.S_PLAYER, (200,200))

    pygame.display.flip()

def game_main_loop(SURFACE_MAIN):
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

    return(SURFACE_MAIN)

if __name__ == "__main__":
    SURFACE_MAIN = game_initialize()
    game_main_loop(SURFACE_MAIN)
