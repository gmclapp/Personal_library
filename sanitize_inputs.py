'''This package allows the user to request input from the user and handles
most error checking and input rules.'''

__version__ = "0.3.0"

import numpy as np
import readchar
from colorama import init

init()

# select function built by Kamik423 in cutie library
def select(
        options,
        deselected_prefix: str = '\033[1m[ ]\033[0m ',
        selected_prefix: str = '\033[1m[\033[32;1mx\033[0;1m]\033[0m ',
        selected_index: int = 0) -> int:
    """Select an option from a list.
    Args:
        options (List[str]): The options to select from.
        deselected_prefix (str, optional): Prefix for deselected option ([ ]).
        selected_prefix (str, optional): Prefix for selected option ([x]).
        selected_index (int, optional): The index to be selected at first.
    Returns:
        int: The index that has been selected.
    """
    print('\n' * (len(options) - 1))
    while 1:
        print(f'\033[{len(options) + 1}A')
        for i, option in enumerate(options):
            print('\033[K{}{}'.format(
                selected_prefix if i == selected_index else deselected_prefix,
                option))
        keypress = readchar.readkey()
        if keypress == readchar.key.UP:
            if selected_index == 0:
                selected_index = len(options) - 1
            else:
                selected_index -= 1
        elif keypress == readchar.key.DOWN:
            if selected_index == len(options) - 1:
                selected_index = 0
            else:
                selected_index += 1
        else:
            break
    return selected_index

class col_vec():
    '''Retrieves a list of real number for x, y, and z from the user,
    and constructs a numpy column vector.'''
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]
        self.vec = np.array([[self.x],[self.y],[self.z]])
        
def get_real_number(prompt=None, upper=float('Inf'), lower=float('-Inf')):
    '''Gets a real number from the user with an optional prompt. Positive and
    negative limits can be set. If not set, the default values are 'Inf' and
    '-Inf' respectively.'''

    num_flag = False
    while(not num_flag):
        try:
            number = float(input(prompt))
            if lower < number < upper:
                num_flag = True
            else:
                print("value must be between {} and {} exclusive.".format(lower, upper))
                print("\033[2A\033[K\033[1A\033[K\r", end='')
            
        except ValueError:
            print("\033[1A\033[K\033[1A\033[K\r", end='')
            num_flag = False
    print("\033[K", end='')        
    return(number)

def get_integer(prompt=None, upper=float('Inf'), lower=float('-Inf')):
    '''Gets an integer from the user with an optional prompt. Positive and
    negative limits can be set. If not set, the default values are 'Inf' and
    '-Inf' respectively.'''
    num_flag = False
    while(not num_flag):
        try:
            number = int(input(prompt))
            number += 0
            # This will throw an exception if number is not an integer.
            
            if lower < number < upper: # excludes endpoints
                num_flag = True
            else:
                print("value must be between {} and {} exclusive.".format(lower, upper))
                print("\033[2A\033[K\033[1A\033[K\r", end='')
            
            
        except ValueError:
            print("\033[1A\033[K\033[1A\033[K\r", end='')
            # \033[K = Erase to the end of line
            # \033[1A = moves the cursor up 1 line.
            # \r = return
            num_flag = False
    print("\033[K", end='')        
    return(number)

def get_letter(prompt=None, accept=None):
    '''Gets a single alpha character that is included in the list 'accept'
    Optionally include a prompt to the user
    omitting the accept list allows all alpha characters.'''

    flag = False
    while(not flag):
        letter = str(input(prompt))
        if(letter.isalpha() and len(letter) == 1):
            if accept != None:
                for i in accept:
                    if letter == i or accept==None:
                        flag = True
                        break
                    else:
                        pass
            else:
                flag = True

        else:
            pass

    return(letter)

def get_coords(rows=3):
    '''This function gets the coordinates for a point in 3D space from the user.
    It includes the error checking logic required to ensure the point's
    useability in subsequent functions.'''

    P_x = get_real_number("X >>> ")
    P_y = get_real_number("Y >>> ")
    P_z = get_real_number("Z >>> ")

    point = col_vec([P_x,P_y,P_z])

    if rows == 3:
        return(point)
    elif rows == 4:
        point.vec = np.row_stack([point.vec,[1]])
        return(point)
    else:
        print("Invalid argument.")
        return(None)
