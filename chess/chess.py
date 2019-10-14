import pygame

def quit_nicely():
    pygame.display.quit()
    pygame.quit()
    
class board():
    def __init__(self):
        self.dark_color = (50, 50, 50)
        self.light_color = (255, 255, 255)
        
        self.square_size = 60
        
        self.light_square = pygame.Surface((self.square_size,self.square_size))
        self.light_square.fill(self.light_color)
        
        self.board_size = self.square_size*8
        self.board = pygame.Surface((self.board_size,self.board_size))
        self.board.fill(self.dark_color)

        for i in range(32):
            if int(i/4)%2:
                self.board.blit(self.light_square,
                                (2*self.square_size*(i%4),
                                 self.square_size*int(i/4)))
            else:
                self.board.blit(self.light_square,
                                (2*self.square_size*(i%4) + self.square_size,
                                 self.square_size*int(i/4)))

    def draw(self, screen):
        screen.blit(self.board, (0,0))
        
def FEN_to_array(FEN):
    board_array = []
                   
    board, turn, castle, enpassant, halfmoves, fullmoves = FEN.split()
    rows = board.split("/")
    for i,row in enumerate(rows):
        for square in row:
            try:
                square = int(square)
                for sq in range(square):
                    board_array.append(".")
            except:
                board_array.append(square)

    print(board_array)
    
def array_to_FEN(array):
    return(FEN)
        
# define a main function
def main():
    
    # initialize the pygame module
    pygame.init()
    
    screen_hgt = 640
    screen_wid = 640
    screen_bg = (73, 106, 117) # grey

    msg = ''
    msg_color = (0, 0, 255) # blue
    
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

    # create board surface
    Board = board()

    # Load chess piece artwork
    art = {'r':pygame.image.load("black rook.png"),
           'n':pygame.image.load("black knight.png"),
           'b':pygame.image.load("black bishop.png"),
           'q':pygame.image.load("black queen.png"),
           'k':pygame.image.load("black king.png"),
           'p':pygame.image.load("black pawn.png"),
           'R':pygame.image.load("white rook.png"),
           'N':pygame.image.load("white knight.png"),
           'B':pygame.image.load("white bishop.png"),
           'Q':pygame.image.load("white queen.png"),
           'K':pygame.image.load("white king.png"),
           'P':pygame.image.load("white pawn.png")}
    
    
    # define a variable to control the main loop
    running = True

    starting_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    FEN_to_array(starting_position)

    v_marcques = "2kr3r/pp3ppp/2pbbq2/4n2Q/4B3/2N4P/PPP2PP1/R2R2K1 w - - 3 17"
    FEN_to_array(v_marcques)
    
    # main loop
    while running:
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                msg = ('X: %.3f, Y: %.3f' %(mx, my))

        #Fill the screen surface object with the specified color
        screen.fill(screen_bg)

        # Render the board
        Board.draw(screen)
        msgBox = fontObj.render(msg, False, msg_color)
        screen.blit(msgBox, (0,0))
        
        # Draw the window to the screen
        pygame.display.flip()

        # Wait long enough to reduce the FPS to 60fps
        fpsClock.tick(60)

    quit_nicely()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()

