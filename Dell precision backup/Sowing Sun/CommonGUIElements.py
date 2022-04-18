import pygame
class Button():
    def __init__(self, parent_surface, label=None, x=0, y=0):
        self.parent_surface = parent_surface
        self.label = label
        self.x=x
        self.y=y
        
        self.status = 'idle'

        self.idle_img = pygame.image.load('art\Button_idle.png')
        self.focused_img = pygame.image.load('art\Button_focused.png')
        self.pressed_img = pygame.image.load('art\Button_pressed.png')

        self.image = self.idle_img                             

    def draw_button(self):
        if(self.status == 'idle'):
            self.image = self.idle_img
        elif(self.status == 'focused'):
            self.image = self.focused_img
        elif(self.status == 'pressed'):
            self.image = self.pressed_img
        
        if self.label != None:
            myFont = pygame.font.SysFont('Courier', 16)
            msg = myFont.render(self.label, True, (255,255,255))
            self.image.blit(msg, (10,10))

        self.parent_surface.blit(self.image, (self.x, self.y))

    def button_status(self, mouse_x, mouse_y, click=0, release=0): #pass mouse location and whether or not location represents a 'click'
                                                                #release, or neither. (can't be both)
        x_crossover = self.x < mouse_x < self.x + 250 #change this line when introducing variable button width.
        y_crossover = self.y < mouse_y < self.y + 100 #change this line when introducting variable button height.

        if(x_crossover
        and y_crossover
        and not click
        and release
        and self.status == 'pressed'):
            return 1
        elif (not x_crossover
        or not y_crossover):
            self.status = 'idle'
            return 0
        elif (x_crossover
        and y_crossover
        and not click):
            self.status = 'focused'
            return 0
        elif (x_crossover
        and y_crossover
        and click
        and not release
        and self.status == 'focused'):
            self.status = 'pressed'
            return 0
        
class screen_message():    
    def __init__(self,parent_surface, msg, font, x=0, y=0, color=(0,255,0), bg=None):
        self.parent_surface = parent_surface
        self.myFont = font
        self.msg = msg
        
        self.x = x
        self.y = y
        self.color = color
        self.bg = bg
        self.surf = self.myFont.render(self.msg, True, self.color, self.bg)
        
    def draw(self):
        self.surf = self.myFont.render(self.msg, True, self.color, self.bg)
        self.parent_surface.blit(self.surf, (self.x,self.y))
