import pygame
import constants
import json

class struct_tile():
    def __init__(self, tile_number):
        self.serial_no = tile_number
        with open("data\\tiles.txt","r") as f:
            tile_list = json.load(f)
            for t in tile_list:
                if t["serial_no"] == self.serial_no:
                    self.name = t["name"]
                    self.block_path = t["block_path"]
                    self.art = pygame.image.load(t["art"])

class element():
    def __init__(self,x,y,sprite,ai=None):
        self.x = x
        self.y = y
        self.sprite = sprite

        if ai:
            self.ai = ai
            ai.owner = self

    def draw(self,surf):
        surf.blit(self.sprite, (self.x*constants.RES, self.y*constants.RES))
        
class actor(element):
    def move(self, dx, dy):
        try:
            dest_tile = game_obj.scene_list[0]["map"][self.y+dy][self.x+dx]
            for t in game_obj.tile_list:
                if t.serial_no == dest_tile:
                    break
                else:
                    pass
            if not t.block_path:
                self.x += dx
                self.y += dy
                game_obj.vars["turn"] += 1
                
            else:
                print("Can't walk there. It's a {}".format(t.name))
                
                
        except IndexError:
            print("Tile out of range")
            
            
        
class prop(element):
    def interact(self):
        pass


class ai():
    def take_turn(self):
        self.owner.move(1,1)
        
class game_object():
    def __init__(self):
        self.SURFACE_MAIN = None
        self.font = pygame.font.Font(None,32)
        self.actor_list = []
        self.prop_list = []
        self.scene_list = []
        self.tile_list = []
        self.vars = {"cheat_codes": False,
                     "cheat_text": '',
                     "page":1,
                     "debug": False,
                     "turn": 0}

    def load(self):
        print("Loading tile data...")
        with open("data\\tiles.txt","r") as f:
            tile_data = json.load(f)
            num_tiles = len(tile_data)
        for i in range(num_tiles):
            self.tile_list.append(struct_tile(i))

        print("Loading scene...")
        with open("scenes\\1.txt","r") as f:
            self.scene_list.append(json.load(f))

            
    def save(self):
        pass
        
        
def quit_nicely():
    pygame.display.quit()
    pygame.quit()

def handle_cheat_code():
    args = game_obj.vars["cheat_text"].split()

    if args[0] == 'tp':
        print("Teleport an actor")
        
        x = args[2]
        y = args[3]

        if args[1] == 'me':
            print("Teleport the character. X={}, Y={}".format(x,y))
            game_obj.actor_list[0].x = int(x)
            game_obj.actor_list[0].y = int(y)
            
        elif args[1] == 'them':
            print("Teleport someone else. X={}, Y={}".format(x,y))
    elif args[0] == 'help':
        print("tp <target> <x> <y> teleports a target to an x,y destination.")
        print("for example: \"tp me 0 0 \" teleports the player to the top left corner of the scene.")

    else:
        print(args)
        
        
        
def draw_game():

    # Background fill to erase previous frame
    game_obj.SURFACE_MAIN.fill(constants.DEFAULT_BG)

    # Render the current scene
    for y,row in enumerate(game_obj.scene_list[0]["map"]):
        for x,tile in enumerate(row):
            for t in game_obj.tile_list:
                if t.serial_no == tile:
                    game_obj.SURFACE_MAIN.blit(t.art,(x*constants.RES,y*constants.RES))
        
    # Draw the side bar menu
    if game_obj.vars["page"] == 1:
        game_obj.SURFACE_MAIN.blit(constants.MENU_FIRST_PAGE,
                                   (constants.SCENE_WIDTH,0))
    elif game_obj.vars["page"] == 2:
        game_obj.SURFACE_MAIN.blit(constants.MENU_MIDDLE_PAGE,
                                   (constants.SCENE_WIDTH,0))
    elif game_obj.vars["page"] == 3:
        game_obj.SURFACE_MAIN.blit(constants.MENU_LAST_PAGE,
                                   (constants.SCENE_WIDTH,0))

    
    # draw the character and other actors
    for a in game_obj.actor_list:
        a.draw(game_obj.SURFACE_MAIN)
        
    # Define input box characteristics, this should be moved such that it doesn't happen
    # every frame.
    input_box_hgt = 32
    input_box = pygame.Rect(0,
                            constants.GAME_HEIGHT-input_box_hgt,
                            constants.GAME_WIDTH,
                            input_box_hgt)

    # Draw the cheat code box if cheat mode is active.
    if game_obj.vars["cheat_codes"]:
        pygame.draw.rect(game_obj.SURFACE_MAIN, constants.CHEAT_TXT_BOX_BG,input_box, 0)
        txt_surface = game_obj.font.render(game_obj.vars["cheat_text"],True,constants.CHEAT_TXT)
        game_obj.SURFACE_MAIN.blit(txt_surface,(input_box.x+5,input_box.y+5))

    # Draw debug information if debug mode is active.
    if game_obj.vars["debug"]:
        debug_text = game_obj.font.render(game_obj.vars["debug_text"],True,constants.DEBUG_TXT)
        game_obj.SURFACE_MAIN.blit(debug_text,(0,0))
        
    # Flip the display to show the next frame
    pygame.display.flip()

def game_main_loop():
    game_quit = False
    fpsClock = pygame.time.Clock()
    
    while not game_quit:
        event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.QUIT:
                game_quit = True

            if event.type == pygame.KEYDOWN and game_obj.vars["cheat_codes"]:
                if event.key == pygame.K_RETURN:
                    handle_cheat_code()
                    game_obj.vars["cheat_text"] = ''
                    game_obj.vars["cheat_codes"] = not game_obj.vars["cheat_codes"]
                elif event.key == pygame.K_BACKSPACE:
                    game_obj.vars["cheat_text"] = game_obj.vars["cheat_text"][:-1]
                else:
                    game_obj.vars["cheat_text"] += event.unicode
                    
            elif event.type == pygame.KEYDOWN and not game_obj.vars["cheat_codes"]:
                if event.key == pygame.K_w:
                    game_obj.actor_list[0].move(0,-1)
                if event.key == pygame.K_a:
                    game_obj.actor_list[0].move(-1,0)
                if event.key == pygame.K_s:
                    game_obj.actor_list[0].move(0,1)
                if event.key == pygame.K_d:
                    game_obj.actor_list[0].move(1,0)
                if event.key == pygame.K_RETURN:
                    game_obj.vars["cheat_codes"] = not game_obj.vars["cheat_codes"]
                if event.key == pygame.K_F3:
                    game_obj.vars["debug"] = not game_obj.vars["debug"]

            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos

        game_obj.vars["debug_text"] = "X: {} Y: {} TILE: ({},{}) TURN: {}".format(mx,my,
                                                                                 int(mx/constants.RES),
                                                                                 int(my/constants.RES),
                                                                                 game_obj.vars["turn"])
                 
        draw_game()
        fpsClock.tick(60)

    quit_nicely()
                
def game_initialize():
    pygame.init()
    game_obj = game_object()

    game_obj.SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH,
                                            constants.GAME_HEIGHT))
    game_obj.load()

    game_obj.actor_list.append(actor(1,1,constants.S_PLAYER))

    return(game_obj)

if __name__ == "__main__":
    game_obj = game_initialize()
    game_main_loop()
