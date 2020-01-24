import random
import constants

class simple_ai():
    def take_turn(self):
        decision = random.randint(0,4)
        if decision == 0: # Don't move
            pass
        elif decision == 1: # Move right
            self.owner.move(1,0)
        elif decision == 2: # Move left
            self.owner.move(-1,0)
        elif decision == 3: # Move up
            self.owner.move(0,-1)
        elif decision == 4: # Move down
            self.owner.move(0,1)
        else:
            print("Indecision!")

class storage():
    def __init__(self, max_slots = 8, inventory = None):
        self.max_slots = max_slots
        if inventory:
            self.inventory = inventory
        else:
            self.inventory = []

    def set_inv_art(self, inv_art):
        self.inv_art = inv_art
        self.anchor_x = self.owner.x*constants.RES - 50
        self.anchor_y = self.owner.y*constants.RES - 75
            
class bipedal_body():
    def __init__(self):
        self.head = body_part(10)
        self.torso = body_part(10)
        self.left_arm = body_part(10)
        self.right_arm = body_part(10)
        self.left_leg = body_part(10)
        self.right_leg = body_part(10)

class body_part():
    def __init__(self,hp):
        self.hp = hp
