import pygame

def quit_nicely():
    pygame.display.quit()
    pygame.quit()
    
class board():
    def __init__(self):
        self.dark_color = (50, 50, 50)
        self.light_color = (255, 255, 255)
        self.square_size = 25
        self.light_square = pygame.Surface()
        self.board = pygame.Surface()
        for i in range(64):
            self.board.blit(pygame.rect(0,0))

    def draw(self, screen, location, size):
        pass
        
        
        
# define a main function
def main():
    
    # initialize the pygame module
    pygame.init()
    
    screen_hgt = 640
    screen_wid = 640
    screen_bg = (73, 106, 117) # grey

    msg = ''
    msg_color = (255, 255, 255) # white
    
    # Create a Font object with a font of size 24 points
    fontObj = pygame.font.Font('freesansbold.ttf', 24)
    
    # The Clock object makes sure the program runs no faster than the specified
    # FPS
    fpsClock = pygame.time.Clock()

    # load and set the logo.
    #logo = pygame.image.load("O2Included\logo_32x32.png")
    #pygame.display.set_icon(logo)
    #pygame.display.set_caption("minimal program")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((screen_wid,screen_hgt))
     
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        #Fill the screen surface object with the specified color
        screen.fill(screen_bg)
        msgBox = fontObj.render(msg, False, msg_color)
        screen.blit(msgBox, (0,0))
                    
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                msg = ('X: %.3f, Y: %.3f' %(mx, my))

        # Draw the window to the screen
        pygame.display.update()

        # Wait long enough to reduce the FPS to 60fps
        fpsClock.tick(60)

    quit_nicely()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()

