import pygame, sys #imports the pygame and sys modules
from pygame.locals import * #pygame.locals has the constants like QUIT, MOUSEMOTION, AND K_ESCAPE.
import random
random.seed()

pygame.init()#This must be called before any other pygame code.
fpsClock = pygame.time.Clock() #The Clock object makes sure our program runs (at most) at a certain FPS.

screen = pygame.display.set_mode((1000,2400)) #set_mode() creates the window. Param is (width, height) in pixels. The Surface object returned is drawn to the screen when pygame.display.update() is called.
pygame.display.set_caption('Pygame helper caption')

red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0) #Params to the Color objects are for Red, Green, Blue. 0 is none.  255 is max
blue = pygame.Color(0,0,255)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
mousex, mousey = 0,0

fontObj = pygame.font.Font('freesansbold.ttf', 24) #Create a Font object with a font of size 32 points
msg = ' '

#car dimensions 168mm by 72mm
car_length = 168
car_height = 72
car_width = 69
pixels_per_unit = 5

class material: #each material unit is 1 square mm
    def __init__(self, name):
        self.name = name
        if self.name == 'Nothing':
            self.density = 0
            self.color = black
            
        elif self.name == 'Aluminum':
            self.density = 2.6989 #g/cc
            self.color = blue

        elif self.name == 'Wood':
            self.density = 0.420 #g/cc
            self.color = green

        elif self.name == 'Steel':
            self.density = 7.87 #g/cc
            self.color = red
            
        self.mass = self.density/1000 #g/mm3
class chunk:
    def __init__(self, mat, x, y):
        self.mat = material(mat)
        self.x = x
        self.y = y
        
class Car:
    def __init__(self, serial_no = None):
        self.body = []
        self.serial_no = serial_no
        self.surf = pygame.Surface((pixels_per_unit*car_length,pixels_per_unit*car_height))
        
    def gen_rand_body(self):
        for i in range(car_length*car_height): #range is car length by height
            temp = random.randint(0,100)
            x = i%car_length
            y = i/car_length
            if temp <= 60:
                new_chunk = chunk('Nothing', x, y)
            elif 60 < temp <= 90:
                new_chunk = chunk('Wood', x, y)
            elif 90 < temp <= 95:
                new_chunk = chunk('Aluminum', x, y)   
            elif 95 < temp <= 100:
                new_chunk = chunk('Steel', x, y)
            self.body.append(new_chunk)
        for chk in self.body:
            pygame.draw.rect(self.surf, chk.mat.color,(chk.x*pixels_per_unit, chk.y*pixels_per_unit, pixels_per_unit, pixels_per_unit))

    def add_body(self, body):
        self.body = body
        for chk in self.body:
            pygame.draw.rect(self.surf, chk.mat.color,(chk.x*pixels_per_unit, chk.y*pixels_per_unit, pixels_per_unit, pixels_per_unit))
            
    def print(self, surface):
        surface.blit(self.surf, (0,0))

    def calc_mass(self):
        self.mass =0
        for chk in self.body:
            self.mass += chk.mat.mass

        self.mass *= car_width #width of the car
        
    def load(self):
        pass
    def save(self):
        pass

    def calc_COM(self):
        self.COMx = 0
        self.COMy = 0
        for chk in self.body:
            self.COMx += chk.x*chk.mat.mass
            self.COMy += chk.y*chk.mat.mass

        self.COMx /= (self.mass/car_width)
        self.COMy /= (self.mass/car_width)
            
class Car_list:
    def __init__(self):
        self.cars = []
    def add(self, car):
        self.cars.append(car)
    def remove(self, car):
        for member in self.cars:
            if member.serial_no == car.serial_no:
                self.cars.remove(member)
            else:
                pass
    def sort(self):
        self.cars = sorted(self.cars, key=lambda car: car.score, reverse=True)

#==========Functions==========#
def Fitness(car_list):
    mass_multiplier = 100
    for car in car_list:
        car.score = 0
        
    #Mass score, maximum allowable mass = 141.748g    
    for car in car_list:
        mass_score = 0
        mass_score = abs(141.748-car.mass)/141.748
        car.score += mass_score*-mass_multiplier    
        
    car_list = sorted(car_list, key=lambda car: car.score, reverse=True)
    for car in car_list:
        print("Car",car.serial_no,"Mass",car.mass,"g, Score:", car.score,"points")
    
def Eliminate_inferior_cars(car_list):
    half = int(len(car_list)/2)
    for i in range(half):
        car_list.pop()
    for car in car_list:
        print("Car",car.serial_no,"Mass",car.mass,"g, Score:", car.score,"points")

def Crossover(car_A, car_B):
    mutation_chance = 0.001 #1% chance of neither parent car's gene being passed
    new_body = []
    for chk in range(len(car_A.body)-1):
        rand = random.random()
        if rand < mutation_chance:
            temp = random.randint(0,3)
            x = chk%car_length
            y = chk/car_length
            if temp == 0:
                new_chunk = chunk('Nothing', x, y)
            elif temp == 1:
                new_chunk = chunk('Aluminum', x, y)
            elif temp == 2:
                new_chunk = chunk('Wood', x, y)   
            elif temp == 3:
                new_chunk = chunk('Steel', x, y)
            new_body.append(new_chunk)
            
        elif rand >= mutation_chance and rand < (1-mutation_chance)/2:
            try:
                new_body.append(car_A.body[chk])
            except IndexError:
                print('Index: ', chk)
        else:
            try:
                new_body.append(car_B.body[chk])
            except IndexError:
                print('Index: ', chk)
            
    return new_body
def Advance_generation(car_list):
    pass

#==========Main==========#
generation = 0
serial_no = 0
active_car = 0
A = Car_list()
for i in range(10):
    new_car = Car(serial_no)
    A.add(new_car)
    serial_no += 1
for car in A.cars:
    car.gen_rand_body()
    car.calc_mass()
    car.calc_COM()

while True:
    screen.fill(black) #This will fill the Surface object with black
    msg = "Active car " + str(active_car)
    msg1 = str(A.cars[active_car].COMx)+' '+str(A.cars[active_car].COMy)
    A.cars[active_car].print(screen)
    
    msgBox = fontObj.render(msg, False, green) #render() creates a surface object with the text drawn on it in the specified font and color. You can blit() this Surface object to the window's Surface object.
    screen.blit(msgBox, (0,410))
    msgBox1 = fontObj.render(msg1, False, green)
    screen.blit(msgBox1, (0,450))
    
    for event in pygame.event.get(): #pygame.event.get() returns a list of all Event objects that happened since the last time get() was called
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION: #The event object has type, pos, key and other attributes depending on the type of event it is.
            mousex, mousey = event.pos
            temp = ('X: %.3f, Y: %.3f' %(mousex, mousey))
##            msg = temp
        elif event.type == MOUSEBUTTONUP:
            mousex, mousey = event.pos
            if event.button == 1:
##                msg = 'Left mouse click'
                Fitness(A.cars)
                A.sort()
                print("\n")
                Eliminate_inferior_cars(A.cars)
                active_car = 0
                

            elif event.button == 2:
                pass
##                msg = 'Middle mouse click'
            elif event.button == 3:
##                msg = 'Right mouse click'
                new_body = Crossover(A.cars[random.randint(0,len(A.cars)-1)],A.cars[random.randint(0,len(A.cars)-1)])
                new_car = Car(serial_no)
                new_car.add_body(new_body)
                new_car.calc_mass()
                new_car.calc_COM()
                A.add(new_car)
                serial_no += 1
                
            elif event.button == 4:
##                msg = 'Mouse scrolled up.'
                pass
            elif event.button == 5:
##                msg = 'Mouse scrolled down.'
                pass
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            elif event.key == K_DOWN: 
                if active_car == len(A.cars)-1:
                    active_car = 0
                else:
                    active_car += 1
            elif event.key == K_UP:
                if active_car == 0:
                    active_car = len(A.cars)-1
                else:
                    active_car -= 1

    pygame.display.update() #The window is not drawn to the actual screen until pygame.display.update is called.
    fpsClock.tick(30) #wait long enough to run at 30 frames per second. (Call this after pygame.display.update().)
            

    
        
