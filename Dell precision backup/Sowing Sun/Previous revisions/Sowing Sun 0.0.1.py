import pygame, sys #imports the pygame and sys modules
from pygame.locals import * #pygame.locals has the constants like QUIT, MOUSEMOTION, AND K_ESCAPE.

pygame.init()#This must be called before any other pygame code.
fpsClock = pygame.time.Clock() #The Clock object makes sure our program runs (at most) at a certain FPS.
framerate = 60

screen = pygame.display.set_mode((640,640)) #set_mode() creates the window. Param is (width, height) in pixels. The Surface object returned is drawn to the screen when pygame.display.update() is called.
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
        
        
##        for col in range(8):
##            self.grid.append(self.row)
####            print('something')
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
    def __init__(self):
        self.position = [50.0,50.0]
        self.destination = [50.0,50.0]
        self.speed = 2
        self.heading = 's'
        self.movestatus = 'stationary'
        self.image = pygame.Surface((32,32))
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
        
    def move(self):
        self.position[0] = self.position[0] + (self.destination[0]-
                                               self.position[0])
        self.position[1] = self.position[1] + (self.destination[1]-
                                               self.position[1])

    def move_status(self):
        movement_keys = a_pressed + w_pressed + d_pressed + s_pressed
        if movement_keys > 0:
            self.movestatus = 'moving'
            if d_pressed:
                self.heading = 'e'
            elif a_pressed:
                self.heading = 'w'
            elif s_pressed:
                self.heading = 's'
            elif w_pressed:
                self.heading = 'n'
        else:
            self.movestatus = 'stationary'
            
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
                print("Heading Error!")
        elif self.movestatus == 'moving':
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
    

fontObj = pygame.font.Font('freesansbold.ttf', 16) #Create a Font object with a font of size 32 points
msg1 = ' '
msg2 = ' '
msg3 = ' '

tile_grass_short = pygame.image.load('art\short_grass_tile.png')
tile_grass_long = pygame.image.load('art\long_grass_tile.png')

Player = Unit()
Player.S_walk1 = pygame.image.load('art\Player_forward1.png')
Player.S_walk2 = pygame.image.load('art\Player_forward2.png')

Player.W_walk1 = pygame.image.load('art\Player_left1.png')
Player.W_walk2 = pygame.image.load('art\Player_left2.png')

Player.E_walk1 = pygame.image.load('art\Player_right1.png')
Player.E_walk2 = pygame.image.load('art\Player_right2.png')

Player.N_walk1 = pygame.image.load('art\Player_back1.png')
Player.N_walk2 = pygame.image.load('art\Player_back2.png')

Player.S = pygame.image.load('art\Player_forward_stationary.png')
Player.W = pygame.image.load('art\Player_left_stationary.png')
Player.E = pygame.image.load('art\Player_right_stationary.png')
Player.N = pygame.image.load('art\Player_back_stationary.png')

A1 = area('A1',0,0)
A1.draw_tiles()


while True:
    screen.fill(black) #This will fill the Surface object with black
    local_area.fill(white)

    qrt_clk = float(int(pygame.time.get_ticks()/250))
    msg2 = 'Clock: ' + str(qrt_clk)
    msg3 = 'FPS: ' + str(framerate)
    msgBox1 = fontObj.render(msg1, False, green) #render() creates a surface object with the text drawn on it in the specified font and color. You can blit() this Surface object to the window's Surface object.
    msgBox2 = fontObj.render(msg2, False, green)
    msgBox3 = fontObj.render(msg3, False, green)
    screen.blit(msgBox1, (0,0))
    screen.blit(msgBox2, (0,20))
    screen.blit(msgBox3, (0,40))

    for event in pygame.event.get(): #pygame.event.get() returns a list of all Event objects that happened since the last time get() was called
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION: #The event object has type, pos, key and other attributes depending on the type of event it is.
            mousex, mousey = event.pos
            msg1 = ('X: %.3f, Y: %.3f' %(mousex, mousey))
            
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
            Player.move_status()
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
        Player.destination[0] -= Player.speed    
    if w_pressed:
        Player.destination[1] -= Player.speed
    if d_pressed:
        Player.destination[0] += Player.speed
    if s_pressed:
        Player.destination[1] += Player.speed
        
    Player.move()
    Player.move_status()
    
    #Display State Update
    
    
    local_area.blit(A1.surface, (1,1))
    local_area.blit(Player.image, (Player.position[0], Player.position[1]))
    
    screen.blit(local_area, (screen_left_offset, screen_top_offset))
    
    pygame.display.update() #The window is not drawn to the actual screen until pygame.display.update is called.
    fpsClock.tick(60)
    framerate = round(fpsClock.get_fps(),2)

    
        

