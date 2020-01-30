import pygame
import constants
import json
import random
import component

class loot_table():
    def __init__(self, table):
        '''This class is initiated with a text file that has a list of
        dictionaries where each list element is an item. Each item is defined
        by a dictionary with keywords "name" and "rarity." from that data
        the loot table is constructed.'''
        self.table = table
        with open(table,"r") as f:
            self.loot_list = json.load(f)

        self.rarity_sum = 0  
        prev_max = -1
        for item in self.loot_list:
            self.rarity_sum += int(item["rarity"])
            item["range_min"] = prev_max+1
            item["range_max"] = prev_max+int(item["rarity"])
            prev_max = item["range_max"]

    def roll(self):
        result = random.randint(0,self.rarity_sum-1)
        print("roll: {}".format(result))
        for item in self.loot_list:
            if item["range_min"]<=result<=item["range_max"]:
                return(item)
        print("Invalid roll!")
            
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
    def __init__(self,
                 x,
                 y,
                 scene,
                 sprite=None,
                 player=False,
                 ai=None,
                 name=None,
                 storage=None):
        
        self.x = x
        self.y = y
        self.scene = scene
        self.sprite = sprite
        self.clicked = False

        self.player = player
        
        self.ai = ai
        if ai:
            ai.owner = self
        self.name = name

        
        self.storage = storage
        if storage:
            storage.owner = self
            
    def draw(self,surf):
        if self.scene == game_obj.vars["current_scene"]:
            surf.blit(self.sprite, (self.x*constants.RES, self.y*constants.RES))
            if self.clicked:
                surf.blit(constants.S_SELECTOR, (self.x*constants.RES, self.y*constants.RES))
            

    def is_clicked(self,x,y):
        dx = (self.x+0.5)*constants.RES - x
        dy = (self.y+0.5)*constants.RES - y

        if (dx**2 + dy**2 ) < (constants.RES/2)**2:
            self.clicked = True
        else:
            self.clicked = False
            
class obj_item(element):
    def __init__(self, x,y, scene,serial_num, inst_name,sprite):
        super().__init__(x,y,scene,sprite)
        self.sn = serial_num
        self.inst_name = inst_name
        self.base_atk = 0.0
        self.base_def = 0.0

    def set_implicit(self, affected_stat, stat_val):
        if affected_stat == "attack":
            self.base_atk += float(stat_val)
        elif affected_stat == "defense":
            self.base_def += float(stat_val)
        else:
            print("Invalid value for affected stat")

    def deposit(self,destination):
        if len(destination.storage.inventory)<destination.storage.max_slots:
            destination.storage.inventory.append(self)
            self.container = destination
            return(True)
        else:
            print("Inventory full!")
            return(False)
        
    def move(self,source,destination):
        if len(destination.storage.inventory)<destination.storage.max_slots:
            destination.storage.inventory.append(item)
            source.storage.inventory.remove(item)
            self.container=destination
            
            return(True)
        else:
            print("Inventory full!")
            return(False)
        
class actor(element):
    def move(self, dx, dy):
        try:
            dest_tile = game_obj.scene_list[game_obj.vars["current_scene"]]["map"][self.y+dy][self.x+dx]
            for t in game_obj.tile_list:
                if t.serial_no == dest_tile:
                    break
                else:
                    pass
            if not t.block_path:
                self.x += dx
                self.y += dy
                return(True)
                
            else:
                print("Can't walk there. It's a {}".format(t.name))
                return(False)
                
                
        except IndexError:
            print("Tile out of range")
            return(False)
            
            
        
class prop(element):
    def __init__(self,x,y,scene,prop_type,state,sprite=None,player=False,ai=None,storage=None):
        super().__init__(x,y,scene,sprite=sprite,player=player,ai=ai,storage=storage)
        self.state = state
        self.prop_type = prop_type
        
    def interact(self):
        
        self.update()
        # This value is checked in order to determine if a player turn is complete
        return(True)

    def update(self):
        pass

class container(prop):
    def interact(self,actor):
        if self.state == "closed":
            self.state = "open"
        elif self.state == "open":
            self.state = "closed"
            
        self.update()
        return(True)

    def update(self):
        if self.prop_type == "chest" and self.state == "closed":
            for i in self.storage.inventory:
                print(i)
            self.sprite = constants.S_CHEST
        elif self.prop_type == "chest" and self.state == "open":
            self.sprite = constants.S_CHEST_OPEN

    def draw(self,surf):
        super().draw(surf)
        if self.state == "open":
            surf.blit(self.storage.inv_art,(self.storage.anchor_x,
                                            self.storage.anchor_y))
            for n, i in enumerate(self.storage.inventory):
                surf.blit(i.sprite,(self.storage.anchor_x + (n%4)*(constants.RES + 3)+4,
                                    int(n/4)*(constants.RES+3) + self.storage.anchor_y + 4))
        elif self.state == "closed":
            pass
        else:
            print("invalid container state")

class portal(prop):
    def __init__(self,x,y,scene,prop_type,state,dest_scene,dest_x,dest_y,sprite=None,player=False,ai=None):
        
        super().__init__(x,y,scene,prop_type,state,sprite,player,ai)
        self.dest_scene = dest_scene
        self.dest_x = dest_x
        self.dest_y = dest_y
        
    def interact(self,actor):
        if self.state == "closed":
            self.state = "open"
        elif self.state == "open":
            self.state = "closed"
            
        self.travel(actor)
        return(True)

    def travel(self,actor):
        game_obj.vars["current_scene"] = self.dest_scene
        game_obj.get_props()
        actor.x = self.dest_x
        actor.y = self.dest_y
        actor.scene = self.dest_scene
        
    def update(self):
        if self.prop_type == "door" and self.state == "closed":
            self.sprite = constants.S_DOOR
        elif self.prop_type == "door" and self.state == "open":
            self.sprite = constants.S_DOOR_OPEN
        
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
                     "turn": 0,
                     "current_scene":0,
                     "serial_number_counter":0,
                     "game_mode":"normal"}
        

    def load(self):
        print("Loading tile data...")
        # Load the data which tells the game what art to render and what
        # The properties of a tile are given a serial number; contains no
        # map data.
        with open("data\\tiles.txt","r") as f:
            tile_data = json.load(f)
            num_tiles = len(tile_data)
        for i in range(num_tiles):
            self.tile_list.append(struct_tile(i))

        # Load the map data, and append tile structures to a list of scenes
        print("Loading scene...")
        with open("scenes\\0.txt","r") as f:
            self.scene_list.append(json.load(f))
        with open("scenes\\1.txt","r") as f:
            self.scene_list.append(json.load(f))

    def build_tables(self):
        self.currency_table = loot_table(constants.TABLE_CURRENCY)
        self.gear_table = loot_table(constants.TABLE_GEAR)
        self.tier_table = loot_table(constants.TABLE_TIER)
        with open(constants.LOOT_PROPERTIES) as f:
            self.loot_properties = json.load(f)

    def roll_loot(self,loot_type):
        if loot_type == 'currency':
            currency = self.currency_table.roll()
            print("rolling currency")
            if currency["name"] != "nothing":
                for i in self.loot_properties:
                    if i["name"] == currency["name"]:
                        if i["name"] == "gold coin":
                            print("gold coin!")
                            sprite = constants.S_GOLD_COIN
                            break
                        elif i["name"] == "silver coin":
                            print("silver coin!")
                            sprite = constants.S_SILVER_COIN
                            break
                        elif i["name"] == "bronze coin":
                            print("bronze coin!")
                            sprite = constants.S_BRONZE_COIN
                            break
                            
                new_item = obj_item(0,0,
                                    self.vars["current_scene"],
                                    game_obj.vars["serial_number_counter"],
                                    i["name"],
                                    sprite)
                
                game_obj.vars["serial_number_counter"] += 1
                return(new_item)
            else:
                return(None)

        elif loot_type == 'gear':
            gear = self.gear_table.roll()
            tier = self.tier_table.roll()

            print("Rolled a {}!".format(gear["base"]))
            print("It is tier {}!".format(tier["tier"]))
            
            if gear["base"] != "nothing":
                for i in self.loot_properties:
                    if i["name"] == gear["base"]:
                        if i["name"] == "sword":
                            sprite = constants.S_SWORD
                            break
                        elif i["name"] == "shield":
                            sprite = constants.S_SHIELD
                            break
                        elif i["name"] == "boots":
                            sprite = constants.S_BOOTS
                            break
                        elif i["name"] == "gloves":
                            sprite = constants.S_GLOVES
                            break
                        elif i["name"] == "helmet":
                            sprite = constants.S_HELMET
                            break
                        elif i["name"] == "belt":
                            sprite = constants.S_BELT
                            break
                        elif i["name"] == "shoulders":
                            sprite = constants.S_SHOULDERS
                            break
                        elif i["name"] == "bracers":
                            sprite = constants.S_BRACERS
                            break
                            
                for t in i["tier"]:
                    if t == tier["tier"]:
                        min_roll,max_roll = i["tier"][t].split("-")
                        stat = random.randint(int(min_roll), int(max_roll))
                        print("Rolled a stat of {}!".format(stat))
                        break
                            
                new_item = obj_item(0,0,
                                    game_obj.vars["serial_number_counter"],
                                    self.vars["current_scene"],
                                    i["name"],
                                    sprite)
                game_obj.vars["serial_number_counter"] += 1
                new_item.set_implicit(i["implicit"],str(stat))
                return(new_item)
                
            
            
    def save(self):
        pass

    def get_props(self):
        self.prop_list = []
        
        for p in self.scene_list[self.vars["current_scene"]]["props"]:
            if p["type"] == "chest":
                inventory = []
                for entry in p["inventory"]:
                    new_item = game_obj.roll_loot(entry)
                    
                    if new_item:
                        print("Rolled {}!".format(new_item.inst_name))
                        inventory.append(new_item)
                
                new_container = container(p["x"],
                                          p["y"],
                                          self.vars["current_scene"],
                                          p["type"],
                                          p["state"],
                                          storage=component.storage())
                for i in inventory:
                    if(i.deposit(new_container)):
                        print("Successfully deposited {}".format(i.inst_name))

                new_container.storage.set_inv_art(constants.CHEST_INVENTORY)
                    
                self.prop_list.append(new_container)

            elif p["type"] == "door":
                self.prop_list.append(portal(p["x"],
                                             p["y"],
                                             self.vars["current_scene"],
                                             p["type"],
                                             p["state"],
                                             p["destination_scene"],
                                             p["destination_x"],
                                             p["destination_y"]))
                
            else:
                print("No data for that kind of prop!")

        for p in self.prop_list:
            p.update()
            
            
class button():
    def __init__(self,x,y,width,height,art=None,action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.art = art
        self.action = action
        self.active = True

    def draw(self,surf):
        if self.art:
            surf.blit(self.art, (self.x, self.y))

    def is_clicked(self,x,y):
        if (self.active and self.x < x < self.x+self.width) and (self.y < y < self.y+self.height):
            self.clicked = True
            return(True)
        else:
            self.clicked = False
            return(False)

    def update(self):
        if self.action:
            self.action()

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

class art():
    def __init__(self,art,x,y,active=True):
        self.x = x
        self.y = y
        self.art = art
        self.active = active
        
class menu():
    def __init__(self,x,y,width,height):
        self.button_list = []
        self.art = []
        self.page = 1
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.first_page = 1
        self.last_page = 4

    def is_clicked(self,x,y):
        if (self.x < x < self.x+self.width) and (self.y < y < self.y+self.height):
            self.clicked = True
            for b in self.button_list:
                if b.is_clicked(x,y):
                    b.update()
            return(True)
        else:
            self.clicked = False
            return(False)

    def add_button(self, button):
        self.button_list.append(button)
        
    def draw(self,surf):
        # Draw background art
        surf.blit(constants.MENU_BACKGROUND,(constants.SCENE_WIDTH,constants.SIDE_HEADER_HEIGHT))

        if self.page == self.first_page:
            surf.blit(constants.MENU_FIRST_PAGE,
                      (constants.SCENE_WIDTH,0))

        elif self.page == self.last_page:
            surf.blit(constants.MENU_LAST_PAGE,
                      (constants.SCENE_WIDTH,0))

        else:
            surf.blit(constants.MENU_MIDDLE_PAGE,
                      (constants.SCENE_WIDTH,0))

        # Render text on top
        header_txt_surface = game_obj.font.render(constants.HEADER_1_STRING,True,constants.MENU_HEADER_TXT)
        game_obj.SURFACE_MAIN.blit(header_txt_surface,(constants.SCENE_WIDTH+constants.PAGE_TURN_HITBOX,
                                                       constants.PAGE_TURN_HITBOX))

        name_text = ""
        for a in game_obj.actor_list:
            if a.clicked:
                name_text = a.name
                break
        for p in game_obj.prop_list:
            if p.clicked:
                name_text = p.prop_type
                break
            
        name_txt_surface = game_obj.font.render(name_text,True,constants.MENU_HEADER_TXT)
        game_obj.SURFACE_MAIN.blit(name_txt_surface,(constants.SCENE_WIDTH+50,constants.SIDE_HEADER_HEIGHT+10))

        for b in self.button_list:
            b.draw(surf)

            

    def advance_page(self):
        self.page += 1
        if self.page > self.last_page:
            self.page = self.last_page

    def return_page(self):
        self.page -= 1
        if self.page < self.first_page:
            self.page = self.first_page
        
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

    elif args[0] == 'roll':
        if args[1] == 'currency':
            print("rolling currency")
            game_obj.roll_loot("currency")
            
        elif args[1] == 'gear':
            print("rolling gear")
            game_obj.roll_loot("gear")

    elif args[0] == 'set':
        if args[1] == 'gamemode':
            if args[2] == 'normal':
                game_obj.vars["game_mode"] = 'normal'
            elif args[2] == 'edit':
                game_obj.vars["game_mode"] = 'edit'
            else:
                print("Invalid game mode.")

    else:
        print(args)
        
        
        
def draw_game():

    # Background fill to erase previous frame
    game_obj.SURFACE_MAIN.fill(constants.DEFAULT_BG)

    # Render the current scene
    for y,row in enumerate(game_obj.scene_list[game_obj.vars["current_scene"]]["map"]):
        for x,tile in enumerate(row):
            for t in game_obj.tile_list:
                if t.serial_no == tile:
                    game_obj.SURFACE_MAIN.blit(t.art,(x*constants.RES,y*constants.RES))

    # Draw the side bar menu
    game_obj.side_menu.draw(game_obj.SURFACE_MAIN)

    # Draw props
    for p in game_obj.prop_list:
        p.draw(game_obj.SURFACE_MAIN)
        
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
    new_click = False
    move_successful = False
    fpsClock = pygame.time.Clock()
    mx = 0
    my = 0

    page_forward = button(constants.GAME_WIDTH-constants.PAGE_TURN_HITBOX,
                          0,
                          constants.PAGE_TURN_HITBOX,
                          constants.PAGE_TURN_HITBOX,
                          action=game_obj.side_menu.advance_page)
    
    page_backward = button(constants.SCENE_WIDTH,
                           0,
                           constants.PAGE_TURN_HITBOX,
                           constants.PAGE_TURN_HITBOX,
                           action=game_obj.side_menu.return_page)

    game_obj.side_menu.add_button(page_forward)
    game_obj.side_menu.add_button(page_backward)

    cave_wall_button = button(constants.SCENE_WIDTH+10,
                              constants.SIDE_HEADER_HEIGHT,
                              32,32,art=pygame.image.load("art/cave_wall.png"))
    with open("data\\tiles.txt","r") as f:
        tile_list = json.load(f)
        for i, t in enumerate(tile_list):
            game_obj.side_menu.add_button(button(constants.SCENE_WIDTH+10+(42*i),
                                                 constants.SIDE_HEADER_HEIGHT,
                                                 32,32,
                                                 art = pygame.image.load(t["art"])))
        
    game_obj.side_menu.add_button(cave_wall_button)
                                                                                                                
    game_obj.get_props()
    
    while not game_quit:
        event_list = pygame.event.get()
        for p in game_obj.prop_list:
            pass
            
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
                    move_successful = game_obj.actor_list[0].move(0,-1)
                if event.key == pygame.K_a:
                    move_successful = game_obj.actor_list[0].move(-1,0)
                if event.key == pygame.K_s:
                    move_successful = game_obj.actor_list[0].move(0,1)
                if event.key == pygame.K_d:
                    move_successful = game_obj.actor_list[0].move(1,0)
                if event.key == pygame.K_RETURN:
                    game_obj.vars["cheat_codes"] = not game_obj.vars["cheat_codes"]
                if event.key == pygame.K_F3:
                    game_obj.vars["debug"] = not game_obj.vars["debug"]
                if event.key == pygame.K_SPACE:
                    for a in game_obj.actor_list:
                        if a.clicked and not a.player:
                            print("Attack!")
                    for p in game_obj.prop_list:
                        if p.clicked:
                            move_successful = p.interact(game_obj.actor_list[0])
                            

            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    new_click = True
                    left_click_x, left_click_y = event.pos
                    
            
        if move_successful:
            game_obj.vars["turn"] += 1
            move_successful = False
            for a in game_obj.actor_list:
                if not a.player and a.scene == game_obj.vars["current_scene"]:
                    a.ai.take_turn()
            
        game_obj.vars["debug_text"] = "X: {} Y: {} TILE: ({},{}) TURN: {}".format(mx,my,
                                                                                 int(mx/constants.RES),
                                                                                 int(my/constants.RES),
                                                                                 game_obj.vars["turn"])
        if new_click:

            if game_obj.side_menu.is_clicked(left_click_x,left_click_y):
                pass
            
            # Check scene area
            elif (0 < left_click_x < constants.SCENE_WIDTH
                and 0 < left_click_y < constants.SCENE_HEIGHT):

                for a in game_obj.actor_list:
                    a.is_clicked(left_click_x,left_click_y)
                    
                    
                for p in game_obj.prop_list:
                    p.is_clicked(left_click_x,left_click_y)
                    
                
            new_click = False
                
                 
        draw_game()
        fpsClock.tick(60)

    quit_nicely()
                
def game_initialize():
    pygame.init()
    game_obj = game_object()

    game_obj.SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH,
                                            constants.GAME_HEIGHT))
    game_obj.load()
    game_obj.build_tables()

    game_obj.actor_list.append(actor(1,1,0,constants.S_PLAYER,player=True,name="Player",storage=component.storage()))
    game_obj.actor_list.append(actor(15,15,0,constants.S_ENEMY,player=False,ai=component.simple_ai(),name="Enemy"))

    game_obj.side_menu = menu(constants.SCENE_WIDTH,0,constants.SIDE_BAR_WIDTH,constants.SIDE_HEADER_HEIGHT)

    return(game_obj)

if __name__ == "__main__":
    game_obj = game_initialize()

    
    game_main_loop()
