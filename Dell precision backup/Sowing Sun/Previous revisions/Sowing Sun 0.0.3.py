import pygame, sys #imports the pygame and sys modules
import CommonGUIElements as GUI
from pygame.locals import * #pygame.locals has the constants like QUIT, MOUSEMOTION, AND K_ESCAPE.

pygame.init()#This must be called before any other pygame code.
fpsClock = pygame.time.Clock() #The Clock object makes sure our program runs (at most) at a certain FPS.
framerate = 60

screen = pygame.display.set_mode((1152,640)) #set_mode() creates the window. Param is (width, height) in pixels. The Surface object returned is drawn to the screen when pygame.display.update() is called.
pygame.display.set_caption('Pygame helper caption')

red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0) #Params to the Color objects are for Red, Green, Blue. 0 is none.  255 is max
blue = pygame.Color(0,0,255)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
mousex, mousey = 0,0

area_sizex = 512
area_sizey = 512
local_area = pygame.Surface((area_sizex,area_sizey))

screen_left_offset = 64
screen_top_offset = 64
grid_resolution = 32

a_pressed = 0
w_pressed = 0
s_pressed = 0
d_pressed = 0

a_pressed_time = 0
w_pressed_time = 0
s_pressed_time = 0
d_pressed_time = 0

a_released_time = 0
w_released_time = 0
s_released_time = 0
d_released_time = 0

a_held = 0
w_held = 0
s_held = 0
d_held = 0

class Menu():
    def __init__(self, parent_surface, x, y):
        self.image = pygame.image.load('art\Paper.png')
        self.x = x
        self.y = y
        self.parent_surface = parent_surface                    

    def draw(self):
         self.parent_surface.blit(self.image, (self.x, self.y))
                                       
class tile():
    def __init__(self, image_index, area, x, y):
        self.surface = pygame.Surface((32,32))
        self.image_index = image_index
        self.area = area
        self.x = x
        self.y = y
        
class area():
    def __init__(self,name, x, y):
        self.surface = pygame.Surface((area_sizex-2, area_sizey-2))
        self.name = name
        self.x = x
        self.y = y
        self.grid = []
        
        self.init_tiles()
    def init_tiles(self):

        for element in range(256):
                self.grid.append(tile(0, self.name, element % 16, element//16 ))
                #print('x: ', self.grid[element].x, 'y: ', self.grid[element].y)

        self.grid[0].image_index = 1
        self.grid[128].image_index = 1
        self.grid[17].image_index = 1
        self.grid[2].image_index = 1
        self.grid[255].image_index = 1
        
    def draw_tiles(self):
        for element in range(256):
            if self.grid[element].image_index==0:
                self.surface.blit(pygame.image.load('art\short_grass_tile.png'), (grid_resolution*self.grid[element].x, grid_resolution*self.grid[element].y))
            elif self.grid[element].image_index==1:
                self.surface.blit(pygame.image.load('art\long_grass_tile.png'), (grid_resolution*self.grid[element].x, grid_resolution*self.grid[element].y))

        
class Unit():
    def __init__(self, x=50.0, y=50.0):
        self.position = [x, y]
        self.destination = [x, y]
        self.speed = 1
        self.heading = 's'
        self.movestatus = 'stationary'
        self.steps = 0
        self.selected = 0
        self.image = pygame.Surface((32,32))
        self.selection_circle = pygame.image.load('art\Selection_circle.png')
        self.S_walk1 = pygame.Surface((32,32))
        self.S_walk2 = pygame.Surface((32,32))

        self.W_walk1 = pygame.Surface((32,32))
        self.W_walk2 = pygame.Surface((32,32))

        self.E_walk1 = pygame.Surface((32,32))
        self.E_walk2 = pygame.Surface((32,32))

        self.N_walk1 = pygame.Surface((32,32))
        self.N_walk2 = pygame.Surface((32,32))

        self.S = pygame.Surface((32,32))
        self.W = pygame.Surface((32,32))
        self.E = pygame.Surface((32,32))
        self.N = pygame.Surface((32,32))

    def init_stats(self):
        self.age = 0
        self.health = 0
        self.hunger = 0
        self.thirst = 0
        self.poop = 0
        self.pee = 0
        
    def move(self, direction=None):

#WASD handling
        if direction == 'n':
            self.destination[1] -= self.speed
        if direction == 'w':
            self.destination[0] -= self.speed
        if direction == 's':
            self.destination[1] += self.speed
        if direction == 'e':
            self.destination[0] += self.speed
        if direction == None:
            self.movestatus = 'stationary'
            pass

#Direction calculation        
        self.deltax = self.destination[0]-self.position[0]
        self.deltay = self.destination[1]-self.position[1]
        self.magnitude = (self.deltax**2 + self.deltay**2)**0.5
#Movement
        if self.magnitude:
            self.position[0] += self.deltax/self.magnitude
            self.position[1] += self.deltay/self.magnitude
            
        if self.magnitude > 0.75:
            self.movestatus = 'moving'
        else:
            self.position[0] = self.destination[0]
            self.position[1] = self.destination[1]
            self.movestatus = 'stationary'        

#Heading determination            
        if self.deltax >= 0 and self.deltay > 0:
            if self.deltax > self.deltay:
                self.heading = 'e'
            elif self.deltax < self.deltay:
                self.heading = 's'

        if self.deltax < 0 and self.deltay > 0:
            if (-1 * self.deltax) > self.deltay:
                self.heading = 'w'
            elif (-1 * self.deltax) < self.deltay:
                self.heading = 's'

        if self.deltax >= 0 and self.deltay <= 0:
            if self.deltax > (-1 * self.deltay):
                self.heading = 'e'
            elif self.deltax < (-1 * self.deltay):
                self.heading = 'n'

        if self.deltax < 0 and self.deltay <= 0:
            if self.deltax > self.deltay:
                self.heading = 'n'
            elif self.deltax < self.deltay:
                self.heading = 'w'       

    def img_update(self):
        if self.movestatus == 'stationary':
            if self.heading == 'n':
                self.image = self.N
            elif self.heading == 'w':
                self.image = self.W
            elif self.heading == 'e':
                self.image = self.E
            elif self.heading == 's':
                self.image = self.S
            else:
                self.image = self.S
                print("Heading Error!")
        elif self.movestatus == 'moving':
            if framerate:
                self.steps += (1/framerate)*4
            if self.heading == 'n':
                if qrt_clk % 2 == 0:
                    self.image = self.N_walk1
                else:
                    self.image = self.N_walk2
            elif self.heading == 'w':
                if qrt_clk % 2 == 0:
                    self.image = self.W_walk1
                else:
                    self.image = self.W_walk2
            elif self.heading == 'e':
                if qrt_clk % 2 == 0:
                    self.image = self.E_walk1
                else:
                    self.image = self.E_walk2
            elif self.heading == 's':
                if qrt_clk % 2 == 0:
                    self.image = self.S_walk1
                else:
                    self.image = self.S_walk2
    def draw(self, surface):
        surface.blit(self.image, (self.position[0], self.position[1]))
        if self.selected:
            surface.blit(self.selection_circle, (self.position[0], self.position[1]))

class Plyr(Unit):
    def load_images(self):
        self.S_walk1 = pygame.image.load('art\Player_forward1.png')
        self.S_walk2 = pygame.image.load('art\Player_forward2.png')

        self.W_walk1 = pygame.image.load('art\Player_left1.png')
        self.W_walk2 = pygame.image.load('art\Player_left2.png')

        self.E_walk1 = pygame.image.load('art\Player_right1.png')
        self.E_walk2 = pygame.image.load('art\Player_right2.png')

        self.N_walk1 = pygame.image.load('art\Player_back1.png')
        self.N_walk2 = pygame.image.load('art\Player_back2.png')

        self.S = pygame.image.load('art\Player_forward_stationary.png')
        self.W = pygame.image.load('art\Player_left_stationary.png')
        self.E = pygame.image.load('art\Player_right_stationary.png')
        self.N = pygame.image.load('art\Player_back_stationary.png')

class Shp(Unit):
    def load_images(self):
        self.S_walk1 = pygame.image.load('art\Sheep_forward1.png')
        self.S_walk2 = pygame.image.load('art\Sheep_forward2.png')

        self.W_walk1 = pygame.image.load('art\Sheep_left1.png')
        self.W_walk2 = pygame.image.load('art\Sheep_left2.png')

        self.E_walk1 = pygame.image.load('art\Sheep_right1.png')
        self.E_walk2 = pygame.image.load('art\Sheep_right2.png')

        self.N_walk1 = pygame.image.load('art\Sheep_back1.png')
        self.N_walk2 = pygame.image.load('art\Sheep_back2.png')

        self.S = pygame.image.load('art\Sheep_forward_stationary.png')
        self.W = pygame.image.load('art\Sheep_left_stationary.png')
        self.E = pygame.image.load('art\Sheep_right_stationary.png')
        self.N = pygame.image.load('art\Sheep_back_stationary.png')
        
    def init_stats(self):
        super(Shp, self).init_stats()
        self.wool = 0
        self.meat = 0
        
    def sense_Unit(self, Unit):
        separationx = Unit.position[0] - self.position[0]
        separationy = Unit.position[1] - self.position[1]
        separation_mag = (separationx**2 + separationy**2)**0.5
        if separation_mag < 100:
            print('Yikes!')
            return (separationx, separationy, separation_mag)
        else:
            return (None)
        
fontObj = pygame.font.Font('C:\Windows\Fonts\MATURASC.TTF', 16) #Create a Font object with a font of size 32 points
message1 = GUI.screen_message(screen, ' ',fontObj, 5, 5, green, None)
message2 = GUI.screen_message(screen, ' ',fontObj, 5, 21, green, None)
message3 = GUI.screen_message(screen, ' ',fontObj, 5, 37, green, None)
message4 = GUI.screen_message(screen, ' ',fontObj, 200, 5, green, None)
                
message5 = GUI.screen_message(screen, ' ', fontObj, 600,100, black, None)
message6 = GUI.screen_message(screen, ' ', fontObj, 600,116, black, None)
message7 = GUI.screen_message(screen, ' ', fontObj, 600,132, black, None)
message8 = GUI.screen_message(screen, ' ', fontObj, 600,148, black, None)
message9 = GUI.screen_message(screen, ' ', fontObj, 600,164, black, None)
message10 = GUI.screen_message(screen, ' ', fontObj, 600,180, black, None)
message11 = GUI.screen_message(screen, ' ', fontObj, 600,196, black, None)
message12 = GUI.screen_message(screen, ' ', fontObj, 600,212, black, None)
message13 = GUI.screen_message(screen, ' ', fontObj, 600,228, black, None)

tile_grass_short = pygame.image.load('art\short_grass_tile.png')
tile_grass_long = pygame.image.load('art\long_grass_tile.png')

Player = Plyr()
Player.init_stats()
Player.load_images()

Sheeplist = []

Sheep = Shp(200.0, 300.0)
##Sheep1 = Shp(100.0, 100.0)

Sheeplist.append(Sheep)
##Sheeplist.append(Sheep1)
##Sheeplist.append(Shp())

for sheep in Sheeplist:
    sheep.load_images()
    sheep.init_stats()

##Sheeplist[1].destination[0] = 50
A1 = area('A1',0,0)
A1.draw_tiles()

sideMenu = Menu(screen, 576, 64)

while True:
    screen.fill(black) #This will fill the Surface object with black
    local_area.fill(white)

    qrt_clk = float(int(pygame.time.get_ticks()/250))
    message2.msg = 'Clock: ' + str(qrt_clk)
    message3.msg = 'FPS: ' + str(framerate)
    message4.msg = 'Steps: ' + str(round(Player.steps,0))

    for event in pygame.event.get(): #pygame.event.get() returns a list of all Event objects that happened since the last time get() was called
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION: #The event object has type, pos, key and other attributes depending on the type of event it is.
            mousex, mousey = event.pos
            message1.msg = ('X: %.3f, Y: %.3f' %(mousex, mousey))

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mousex, mousey = event.pos
                selx = mousex-screen_left_offset
                sely = mousey-screen_top_offset
                crossoverx = Player.position[0] < selx < Player.position[0]+grid_resolution
                crossovery = Player.position[1] < sely < Player.position[1]+grid_resolution
                if crossoverx and crossovery:
                    Player.selected = 1
                else:
                    Player.selected = 0
                for sheep in Sheeplist:
                    crossoverx = sheep.position[0] < selx < sheep.position[0]+grid_resolution
                    crossovery = sheep.position[1] < sely < sheep.position[1]+grid_resolution
                    if crossoverx and crossovery:
                        sheep.selected = 1
                    else:
                        sheep.selected = 0
                                  
            elif event.button == 2:
                mousex, mousey = event.pos
                Sheeplist.append(Shp(mousex-screen_left_offset, mousey-screen_top_offset))
                Sheeplist[-1].load_images()
                Sheeplist[-1].init_stats()
                
            elif event.button == 3:
                mousex, mousey = event.pos
                Player.destination[0] = mousex-screen_left_offset
                Player.destination[1] = mousey-screen_top_offset
        elif event.type == MOUSEBUTTONUP:
            mousex, mousey = event.pos
            if event.button == 1:
                msg = 'Left mouse click'
            elif event.button == 2:
                msg = 'Middle mouse click'
            elif event.button == 3:
                msg = 'Right mouse click'
            elif event.button == 4:
                msg = 'Mouse scrolled up.'
            elif event.button == 5:
                msg = 'Mouse scrolled down.'
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
                
            if event.key == K_a:                
                a_pressed = 1
                a_pressed_time = qrt_clk
                print('A Pressed: ' , a_pressed_time)
                
            if event.key == K_w:               
                w_pressed = 1
                w_pressed_time = qrt_clk
                print('W Pressed: ' , w_pressed_time)
                
            if event.key == K_d:              
                d_pressed = 1
                d_pressed_time = qrt_clk
                print('D Pressed: ' , d_pressed_time)
                
            if event.key == K_s:               
                s_pressed = 1
                s_pressed_time = qrt_clk
                print('S Pressed: ' , s_pressed_time)
                
        elif event.type == KEYUP:
            Player.img_update()
            if event.key == K_a:                
                a_pressed = 0
                a_released_time = qrt_clk
                print('A Released: ' , a_released_time)
                
            if event.key == K_w:                
                w_pressed = 0
                w_released_time = qrt_clk
                print('W Released: ' , w_released_time)
                
            if event.key == K_d:                
                d_pressed = 0
                d_released_time = qrt_clk
                print('D Released: ' , d_released_time)
                
            if event.key == K_s:
                
                s_pressed = 0
                s_released_time = qrt_clk
                print('S Released: ' , s_released_time)
            
                
    #Game State Update

        
    if a_pressed:
        Player.move('w')
    if w_pressed:
        Player.move('n')
    if d_pressed:
        Player.move('e')
    if s_pressed:
        Player.move('s')
    if (not a_pressed
        and not w_pressed
        and not d_pressed
        and not s_pressed):
        Player.move()
    
    Player.img_update()

    for sheep in Sheeplist:
        reactx = 0
        reacty = 0
        reactmag = 1
        try:
            reactx,reacty,reactmag = sheep.sense_Unit(Player)
        except:
            pass
        sheep.destination[0] -= reactx/reactmag
        sheep.destination[1] -= reacty/reactmag
        sheep.move()
        sheep.img_update()
        if sheep.selected:
            message5.msg = 'Steps: ' + str(round(sheep.steps,0))
            message6.msg = 'Age: ' + str(sheep.age)
            message7.msg = 'Health: ' + str(sheep.health)
            message8.msg = 'Wool: ' + str(sheep.wool)
            message9.msg = 'Hunger: ' + str(sheep.hunger)
            message10.msg = 'Thirst: ' + str(sheep.thirst)
            message11.msg = 'Meat: ' + str(sheep.meat)
            message12.msg = 'Poop: ' + str(sheep.poop)
            message13.msg = 'Pee: ' + str(sheep.pee)
    #Display State Update
    
    
    local_area.blit(A1.surface, (1,1))
    Player.draw(local_area)
    for sheep in Sheeplist:
        sheep.draw(local_area)

    screen.blit(local_area, (screen_left_offset, screen_top_offset))

    sideMenu.draw()

    message1.draw()
    message2.draw()
    message3.draw()
    message4.draw()
    message5.draw()
    message6.draw()
    message7.draw()
    message8.draw()
    message9.draw()
    message10.draw()
    message11.draw()
    message12.draw()
    message13.draw()
    
    pygame.display.update() #The window is not drawn to the actual screen until pygame.display.update is called.
    fpsClock.tick(60)
    framerate = round(fpsClock.get_fps(),2)

    
        

