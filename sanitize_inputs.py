'''This package allows the user to request input from the user and handles
most error checking and input rules.'''

__version__ = "0.1.2"

import numpy as np

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
                print("Enter a real number between",lower,"and",upper)
            
            
        except ValueError:
            print("Enter a real number.")
            num_flag = False
            
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
            
            if lower < number < upper:
                num_flag = True
            else:
                print(prompt,lower,"and",upper)
            
            
        except ValueError:
            print("Enter an integer.")
            num_flag = False
            
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
