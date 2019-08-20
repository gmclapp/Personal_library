import pygame
import constants
import json

class struct_tile():
    def __init__(self, tile_number):
        pass
        # Based on tile number get a tile definition to set its image and
        # whether it is blocking.
        # self.block_path = block_path

class actor():
    def __init__(self,x,y,sprite):
        self.x = x
        self.y = y
        self.sprite = sprite

    def draw(self,surf):
        surf.blit(self.sprite, (self.x*constants.RES, self.y*constants.RES))

    def move(self, dx, dy):
##        if GAME_MAP[self.x + dx][self.y+dy].block_path == False:
        self.x += dx
        self.y += dy

class game_object():
    def __init__(self):
        self.actor_list = []
        self.scene_list = []
        self.tile_list = []

    def load(self):
        print("Loading tile data...")
        with open("data\\tiles.txt","r") as f:
            self.tile_list = json.load(f)

            
    def save(self):
        pass
        

def map_create():
    new_map = [[struct_tile(False) for y in range(0,30)]for x in range(0,30)]
    new_map[10][10].block_path = True
    new_map[10][15].block_path = True
    return(new_map)
        
def quit_nicely():
    pygame.display.quit()
    pygame.quit()
    
def draw_game(game_obj):

    game_obj.SURFACE_MAIN.fill(constants.DEFAULT_BG)

    # draw the scene

    # draw the character
    for a in game_obj.actor_list:
        game_obj.SURFACE_MAIN.blit(a.sprite, (a.x*constants.RES,a.y*constants.RES))

    pygame.display.flip()

def game_main_loop(game_obj):
    game_quit = False
    cheat_codes = False
    fpsClock = pygame.time.Clock()
    
    while not game_quit:
        event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.QUIT:
                game_quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    game_obj.actor_list[0].move(0,-1)
                if event.key == pygame.K_a:
                    game_obj.actor_list[0].move(-1,0)
                if event.key == pygame.K_s:
                    game_obj.actor_list[0].move(0,1)
                if event.key == pygame.K_d:
                    game_obj.actor_list[0].move(1,0)
                    
        draw_game(game_obj)
        fpsClock.tick(60)

    quit_nicely()
                
def game_initialize():
    pygame.init()
    game_obj = game_object()

    game_obj.SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH,
                                            constants.GAME_HEIGHT))
    game_obj.map = map_create()
    game_obj.load()

    game_obj.actor_list.append(actor(7,7,constants.S_PLAYER))

    return(game_obj)

if __name__ == "__main__":
    game_obj = game_initialize()
    game_main_loop(game_obj)
