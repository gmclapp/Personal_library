import random

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

class container():
    def __init__(self, max_volume = 10.0, intentory = None):
        self.inventory = inventory
        self.max_volume = max_volume
        if inventory:
            self.inventory = inventory
        else:
            self.inventory = []

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
