import pygame, sys #imports the pygame and sys modules
from pygame.locals import * #pygame.locals has the constants like QUIT, MOUSEMOTION, AND K_ESCAPE.

pygame.init()#This must be called before any other pygame code.
fpsClock = pygame.time.Clock() #The Clock object makes sure our program runs (at most) at a certain FPS.

screen = pygame.display.set_mode((640,480)) #set_mode() creates the window. Param is (width, height) in pixels. The Surface object returned is drawn to the screen when pygame.display.update() is called.
pygame.display.set_caption('Pygame helper caption')

red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0) #Params to the Color objects are for Red, Green, Blue. 0 is none.  255 is max
blue = pygame.Color(0,0,255)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
mousex, mousey = 0,0

fontObj = pygame.font.Font('freesansbold.ttf', 24) #Create a Font object with a font of size 32 points
msg = ' '

while True:
    screen.fill(black) #This will fill the Surface object with black

    msgBox = fontObj.render(msg, False, green) #render() creates a surface object with the text drawn on it in the specified font and color. You can blit() this Surface object to the window's Surface object.
    screen.blit(msgBox, (0,0))

    for event in pygame.event.get(): #pygame.event.get() returns a list of all Event objects that happened since the last time get() was called
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION: #The event object has type, pos, key and other attributes depending on the type of event it is.
            mousex, mousey = event.pos
            temp = ('X: %.3f, Y: %.3f' %(mousex, mousey))
            msg = temp
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

    pygame.display.update() #The window is not drawn to the actual screen until pygame.display.update is called.
    fpsClock.tick(30) #wait long enough to run at 30 frames per second. (Call this after pygame.display.update().)
            

    
        
