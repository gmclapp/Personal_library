import pygame
from pygame.locals import *

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

class Position():
    def __init__(self, FEN):
        self.board_array = []
        self.FEN = FEN

    def draw(self, screen):
        for square in self.board_array:
            pass

    def FEN_to_array(self):
                   
        board, self.turn, self.castle, self.enpassant, self.halfmoves, self.fullmoves = self.FEN.split()
        rows = board.split("/")
        for i,row in enumerate(rows):
            for square in row:
                try:
                    square = int(square)
                    for sq in range(square):
                        self.board_array.append(".")
                except:
                    self.board_array.append(square)

    def piece_on_square(self, square):
        '''Takes a algebraic representation of a square and returns the piece on that square.
        None if no piece is present on that square.'''

        try:
            file, rank = list(square)
        except ValueError:
            print("Invalid square, specify letter rank, and number file.")

        ord_file = ord(file.lower()) - 96
        rank = int(rank)
        
        if ord_file > 8 or ord_file < 1:
            print("{} is not a valid file.".format(file))
        if rank > 8 or rank < 1:
            print("{} is not a valid rank.".format(rank))

        board_index = (8-rank)*8 + ord_file-1
        piece = self.board_array[board_index]
        if piece == '.':
            piece = None
            
        return(piece)

    def check_file(self,pos):
        '''Takes a position and returns all the pieces on the same file and
        their positions.'''

        try:
            file, rank = list(pos)
        except ValueError:
            print("Invalid square, specify letter rank, and number file.")
        
        pieces = []
        for i in range(8):
            rank = i+1
            square = file + str(rank)
            piece = self.piece_on_square(square)
            if piece != None:
                pieces.append((square,piece))

        return(pieces)
        
    def check_rank(self,pos):
        '''Takes a position and returns all the pieces on the same rank and
        their positions.'''

        try:
            file, rank = list(pos)
        except ValueError:
            print("Invalid square, specify letter rank, and number file.")

        rank = int(rank)
        
        pieces = []
        for i in range(8):
            file = chr(i + 96 + 1)
            # ASCII position of lower case numbers. + 1 to compensate for i
            # starting at 0
            square = file + str(rank)            
            piece = self.piece_on_square(square)
            if piece != None:
                pieces.append((square, piece))

        return(pieces)
    
    def check_diag(self,pos):
        '''checks both diagonals containing the given position for other pieces
        and returns those pieces and their positions.'''

        try:
            file, rank = list(pos)
        except ValueError:
            print("Invalid square, specify letter rank, and number file.")

        ord_file = ord(file.lower()) - 96
        rank = int(rank)

        squares = [pos]
        f = ord_file
        r = rank
        
        # squares on the same diagonal can be found by adding or subtracting
        # the same integer from both the rank and file. There will be between
        # 8 and 15 squares sharing a diagonal with a given square.
        
        for i in range(8):
            f -= 1
            r -= 1
            if r >= 1 and r >= 1:
                squares.append(chr(f + 96) + str(r))
            else:
                break
        f = ord_file
        r = rank
        for i in range(8):
            f += 1
            r += 1
            if r <= 8 and f <= 8:
                squares.append(chr(f + 96) + str(r))
            else:
                break
        f = ord_file
        r = rank
        for i in range(8):
            f += 1
            r -= 1
            if r >= 1 and f <= 8:
                squares.append(chr(f + 96) + str(r))
            else:
                break
        f = ord_file
        r = rank
        for i in range(8):
            f -= 1
            r += 1
            if r <= 8 and f >= 1:
                squares.append(chr(f + 96) + str(r))
            else:
                break

        print(squares)
        pieces = []
        for s in squares:
            piece = self.piece_on_square(s)
            if piece != None:
                pieces.append((s, piece))
        return(pieces)
        
        
    def check_knight(self,pos):
        '''Checks for knights attacking the given square. Returns those knights
        and their positions'''
        try:
            file, rank = list(pos)
        except ValueError:
            print("Invalid square, specify letter rank, and number file.")

        ord_file = ord(file.lower()) - 96
        rank = int(rank)

        squares = []
        f = ord_file
        r = rank

        f = ord_file + 2
        r = rank + 1
        if (r >= 1 and f >= 1) and (r <= 8 and f <= 8):
            squares.append(chr(f + 96) + str(r))

        f = ord_file + 2
        r = rank - 1
        if (r >= 1 and f >= 1) and (r <= 8 and f <= 8):
            squares.append(chr(f + 96) + str(r))

        f = ord_file - 2
        r = rank + 1
        if (r >= 1 and f >= 1) and (r <= 8 and f <= 8):
            squares.append(chr(f + 96) + str(r))

        f = ord_file - 2
        r = rank - 1
        if (r >= 1 and f >= 1) and (r <= 8 and f <= 8):
            squares.append(chr(f + 96) + str(r))

        f = ord_file + 1
        r = rank + 2
        if (r >= 1 and f >= 1) and (r <= 8 and f <= 8):
            squares.append(chr(f + 96) + str(r))

        f = ord_file - 1
        r = rank + 2
        if (r >= 1 and f >= 1) and (r <= 8 and f <= 8):
            squares.append(chr(f + 96) + str(r))

        f = ord_file + 1
        r = rank - 2
        if (r >= 1 and f >= 1) and (r <= 8 and f <= 8):
            squares.append(chr(f + 96) + str(r))

        f = ord_file - 1
        r = rank - 2
        if (r >= 1 and f >= 1) and (r <= 8 and f <= 8):
            squares.append(chr(f + 96) + str(r))
        
        pieces = []
        for s in squares:
            piece = self.piece_on_square(s)
            if piece != None:
                pieces.append((s, piece))
        return(pieces)

    def get_king_pos(self):
        white_king_found = False
        black_king_found = False
        for i,sq in enumerate(self.board_array):
            if sq == 'k':
                f = (i % 8) + 1
                r = int(8 - i/8) + 1
                black_king = chr(f + 96) + str(r)
                print("found black king {}".format(black_king))
                black_king_found = True
            elif sq == 'K':
                f = (i % 8) + 1
                r = int(8 - i/8) + 1
                white_king = chr(f + 96) + str(r)
                print("found white king {}".format(white_king))
                white_king_found = True
            else:
                pass
                
            if white_king_found and black_king_found:
                break
            else:
                pass
        return(white_king,black_king)

    def is_check(self):
        w_king, b_king = self.get_king_pos()
        white_check = False
        black_check = False

        for p in self.check_rank(w_king):
            if p[1] == 'r' or p[1] == 'q':
                print("Potential threat: {} on {}".format(p[1],p[0]))
        
##        self.check_file(w_king)
##        self.check_knight(w_king)
##
        for p in self.check_rank(b_king):
            if p[1] == 'R' or p[1] == 'Q':
                print("Potential threat: {} on {}".format(p[1],p[0])
                      
##        self.check_file(b_king)
##        self.check_knight(b_king)
        
        if white_check:
            return(-1)
        elif black_check:
            return(1)
        else:
            return(0)
        
    
class game():
    def __init__(self, PGN):
        self.positions = [Position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")]
        self.pgn = PGN
        
        
# define a main function
def main():
    
    # initialize the pygame module
    pygame.init()
    
    screen_hgt = 640
    screen_wid = 640
    start_size = [screen_wid,screen_hgt]
    screen_bg = (73, 106, 117) # grey

    msg = ''
    msg_color = (0, 0, 255) # blue
    
    # Create a Font object with a font of size 24 points
    fontObj = pygame.font.Font('freesansbold.ttf', 24)
    
    # The Clock object makes sure the program runs no faster than the specified
    # FPS
    fpsClock = pygame.time.Clock()

    # load and set the logo.
    logo = pygame.image.load("board_node_icon.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Chess Permutations")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode(start_size, RESIZABLE)

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

    starting_position = Position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    
    starting_position.FEN_to_array()

    v_marcques = Position("2kr3r/pp3ppp/2pbbq2/4n2Q/4B3/2N4P/PPP2PP1/R2R2K1 w - - 3 17")
    v_marcques.FEN_to_array()
    
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

            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    click_x, click_y = event.pos
                    f = chr(int(click_x / Board.square_size) + 97)
                    r = 8 - int(click_y / Board.square_size)

                    print("Clicked {}{}".format(f,r))

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

