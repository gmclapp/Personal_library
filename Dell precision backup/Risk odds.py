import random
#A risk game board has 42 territories
#North America: 9
#South America: 4
#Europe: 7
#Africa: 6
#Asia: 12
#Australia: 4



class territory():
    def __init__(self, name, sn, continent, connections, owner = None, armies = 0):
        self.NAME = name
        self.SERIAL_NUMBER = sn 
        self.CONTINENT = continent
        self.CONNECTIONS = [] #list of tuples with serial numbers of territories at endpoints
        self.owner = owner#current owner of the territory
        self.armies = armies#number of armies present in the territory
        
def roll_dice(num_dice):
    roll = []
    for i in range(num_dice):
        roll.append(random.randint(1,6))

    list.sort(roll,reverse = True)#order dice from largest to smallest

    return roll

def print_roll(roll):
    for die in roll:
        print(die)

def compare_rolls(atk, dfn):#atk is the attack roll, dfn is the defense roll
    length = min(len(atk),len(dfn))
    score = 0
    #there are three possible outcomes:
    #0: defender loses both comparisons
    #-1: attacker and defender each lose one comparison
    #-2: attacker loses both comparisons
    for i in range(length):
        if atk[i] <= dfn[i]:
            score -= 1
            
    return(atk, dfn, score)

Territory_list = []
Territory_list.append(territory("Alaska",1,"North America",[36,2,3]))
Territory_list.append(territory("Northwestern Territory",2,"North America",[1,3,4,9]))
Territory_list.append(territory("Alberta",3,"North America",[1,2,4,6]))
Territory_list.append(territory("Ontario",4,"North America",[2,3,6,7,5,9]))
Territory_list.append(territory("Quebec",5,"North America",[4,7,9]))
Territory_list.append(territory("Western United States",6,"North America",[3,4,7,8]))
Territory_list.append(territory("Eastern United States",7,"North America",[4,5,6,8]))
Territory_list.append(territory("Central America",8,"North America",[6,7,10]))
Territory_list.append(territory("Greenland",9,"North America",[2,4,5,14]))

Territory_list.append(territory("Venezuela",10,"South America",[8,11,12]))
Territory_list.append(territory("Peru",11,"South America",[10,12,13]))
Territory_list.append(territory("Brazil",12,"South America",[10,11,13]))
Territory_list.append(territory("Argentina",13,"South America",[11,12]))

Territory_list.append(territory("Iceland",14,"Europe",[9,15,17]))
Territory_list.append(territory("Great Britain",15,"Europe",[14,16,17,18]))
Territory_list.append(territory("Western Europe",16,"Europe",[15,18,19]))
Territory_list.append(territory("Scandinavia",17,"Europe",[14,15,18,20]))
Territory_list.append(territory("Northern Europe",18,"Europe",[15,16,17,19,20]))
Territory_list.append(territory("Southern Europe",19,"Europe",[16,18,20,21,22,27]))
Territory_list.append(territory("Ukraine",20,"Europe",[17,18,19,27,28,29]))




WW = 0
WL = 0
LL = 0

iterations = 100000
for rounds in range(iterations): 
    attack_roll = roll_dice(3)
    def_roll = roll_dice(2)

    attack_roll, def_roll, outcome = compare_rolls(attack_roll, def_roll)
    if outcome == 0:
        WW+=1
    elif outcome == -1:
        WL+=1
    elif outcome == -2:
        LL+=1

WWodds = WW*100/iterations  
WLodds = WL*100/iterations
LLodds = LL*100/iterations
print("Attacker rolls 3, Defender rolls 2.")
print("WW",WWodds,"WL",WLodds,"LL",LLodds)

WW = 0
WL = 0
LL = 0

for rounds in range(iterations): 
    attack_roll = roll_dice(3)
    def_roll = roll_dice(1)

    attack_roll, def_roll, outcome = compare_rolls(attack_roll, def_roll)
    if outcome == 0:
        WW+=1
    elif outcome == -1:
        WL+=1
    elif outcome == -2:
        LL+=1

WWodds = WW*100/iterations  
WLodds = WL*100/iterations
LLodds = LL*100/iterations
print("Attacker rolls 3, Defender rolls 1.")
print("WW",WWodds,"WL",WLodds,"LL",LLodds)

WW = 0
WL = 0
LL = 0

for rounds in range(iterations): 
    attack_roll = roll_dice(2)
    def_roll = roll_dice(2)

    attack_roll, def_roll, outcome = compare_rolls(attack_roll, def_roll)
    if outcome == 0:
        WW+=1
    elif outcome == -1:
        WL+=1
    elif outcome == -2:
        LL+=1

WWodds = WW*100/iterations  
WLodds = WL*100/iterations
LLodds = LL*100/iterations
print("Attacker rolls 2, Defender rolls 2.")
print("WW",WWodds,"WL",WLodds,"LL",LLodds)

WW = 0
WL = 0
LL = 0

for rounds in range(iterations): 
    attack_roll = roll_dice(2)
    def_roll = roll_dice(1)

    attack_roll, def_roll, outcome = compare_rolls(attack_roll, def_roll)
    if outcome == 0:
        WW+=1
    elif outcome == -1:
        WL+=1
    elif outcome == -2:
        LL+=1

WWodds = WW*100/iterations  
WLodds = WL*100/iterations
LLodds = LL*100/iterations
print("Attacker rolls 2, Defender rolls 1.")
print("WW",WWodds,"WL",WLodds,"LL",LLodds)

WW = 0
WL = 0
LL = 0

for rounds in range(iterations): 
    attack_roll = roll_dice(1)
    def_roll = roll_dice(2)

    attack_roll, def_roll, outcome = compare_rolls(attack_roll, def_roll)
    if outcome == 0:
        WW+=1
    elif outcome == -1:
        WL+=1
    elif outcome == -2:
        LL+=1

WWodds = WW*100/iterations  
WLodds = WL*100/iterations
LLodds = LL*100/iterations
print("Attacker rolls 1, Defender rolls 2.")
print("WW",WWodds,"WL",WLodds,"LL",LLodds)

WW = 0
WL = 0
LL = 0

for rounds in range(iterations): 
    attack_roll = roll_dice(1)
    def_roll = roll_dice(1)

    attack_roll, def_roll, outcome = compare_rolls(attack_roll, def_roll)
    if outcome == 0:
        WW+=1
    elif outcome == -1:
        WL+=1
    elif outcome == -2:
        LL+=1

WWodds = WW*100/iterations  
WLodds = WL*100/iterations
LLodds = LL*100/iterations
print("Attacker rolls 1, Defender rolls 1.")
print("WW",WWodds,"WL",WLodds,"LL",LLodds)
##    print("Attack roll:")
##    print_roll(attack_roll)
##    print("Defense roll:")
##    print_roll(def_roll)
##    print("Score:", outcome)

