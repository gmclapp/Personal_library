import random
import time

random.seed(time.time())

def fight():
    # Defense die rolls
    d1 = random.randint(1,6)
    d2 = random.randint(1,6)

    # Offense die rolls
    d3 = random.randint(1,6)
    d4 = random.randint(1,6)
    d5 = random.randint(1,6)

    # Find the highest of the two dice for offense
    atk_dice = sorted([d3,d4,d5],reverse=True)
    atk_dice.pop(-1)

    # sort the dice for the defense so the highest and lowest respectively are compared
    def_dice = sorted([d1,d2],reverse=True)

    for d in range(len(def_dice)):
        if def_dice[d] >= atk_dice[d]:
            return(0)
        else:
            return(1)

n = 10000
off_tally = 0
def_tally = 0

class territory():
    def __init__(self, serial_number, name, continent, edges):
        self.serial = serial_number
        self.name = name
        self.continent = continent
        self.edges = edges # list of territories directly connected to this one

    def set_player(self, player):
        self.player = player
        # serial number of player who controls this territory
        

if __name__ == "__main__":
    for k in range(n):
        result = fight()
        if result:
            off_tally += 1
        else:
            def_tally += 1

    print("Of {} games, Offense wins {}, Defense wins {}".format(n, off_tally,def_tally))
