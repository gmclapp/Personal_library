import sys
import math

## ---------- Class definitions ---------- ##
class robot():
    def __init__(self,bot_id,x,y,item):
        self.bot_id = bot_id
        self.x = x
        self.y = y
        self.item = item
        self.dest_x = x
        self.dest_y = y
        self.job_x = x
        self.job_y = y
        self.job = "IDLE"
        self.timeout = 0
        self.home = True
        self.action = "WAIT"
        self.radar_flag = False
        self.trap_flag = False
        self.dig_timeout = 7
    
    def act(self):
        if self.action == "WAIT":
            print("WAIT")
        elif self.action == "MOVE":
            print("MOVE",self.dest_x,self.dest_y)
        elif self.action == "DIG":
            print("DIG {} {} {}".format(self.dest_x,self.dest_y,"Digging"+str(self.dest_x)+str(self.dest_y)))
        elif self.action == "REQUEST":
            if self.job == "SURVEYOR":
                print("REQUEST RADAR Surveyor")
            elif self.job == "TRAPPER":
                print("REQUEST TRAP Trapper")
    
    def speak(self):
        print("ID:{},JOB:{},ITEM:{}".format(self.bot_id,self.job,self.item),file = sys.stderr)
        
        
    def set_destination(self,x,y):
        self.dest_x = x
        self.dest_y = y
        
    def mine(self, o_list):
        if len(o_list) != 0:
            for o in o_list:
                if not o.reserved and not o.complete and not o.trapped:
                    x,y,dig_delay = o.reserve()
                    self.set_destination(x,y)
                    self.dig_delay = dig_delay
                    self.job = "MINER"
                    break
                
        if self.job == "IDLE":
            return(False)
        else:
            return(True)
                
    def survey(self, r_list):
        if len(r_list) != 0:
            for r in r_list:
                if not r.reserved and not r.complete:
                    x,y = r.reserve()
                    self.set_destination(x,y)
                    self.job_x = x
                    self.job_y = y
                    self.radar_flag = False
                    self.job = "SURVEYOR"
                    break
                
        if self.job == "IDLE":
            return(False)
        else:
            return(True)
    
    def trap(self, t_list):
        if len(t_list) != 0:
            for t in t_list:
                if not t.reserved and not t.complete:
                    x,y = t.reserve()
                    self.set_destination(x,y)
                    self.job_x = x
                    self.job_y = y
                    self.trap_flag = False
                    self.job = "TRAPPER"
                    break
                
        if self.job == "IDLE":
            return(False)
        else:
            return(True)

class job_site():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reserved = False
        self.complete = False
        self.trapped = False
        self.score = 0
        
    def distance(self,x,y):
        self.d = (self.x - x)**2 + (self.y - y)**2
    
    def calc_score(self):
        self.score = (29 - self.x)/29 # sites closer to the base get priority
         # sites closer to the last robot to run the distance function get priority
        self.score += (1037 - self.d)/1037
        
    def reserve(self):
        self.reserved = True
        return(self.x, self.y)
        
    def release(self, complete=True):
        self.reserved=False
        if complete:
            self.complete = complete
        
class ore_site(job_site):
    def __init__(self, x, y, ore, hole=False):
        super().__init__(x,y)
        self.ore = int(ore)
        if self.ore <=0:
            self.complete=True
        self.hole = hole
        self.dig_timeout = self.x/4 + 1
        
    def calc_score(self):
        super().calc_score()
        if self.hole:
            self.score -= 0.2
            
        
    def reserve(self):
        x,y = super().reserve()
        return(x,y,self.dig_timeout)
        
    def release(self,complete=True):
        self.ore -= 1
        if self.ore <= 0 or complete:
            self.complete = True
        self.reserved = False
        
    def update(self,ore,hole):
        self.ore = int(ore)
        self.hole = hole
        if self.ore <= 0:
            self.complete = True
        else:
            self.complete = False
            
class radar_site(job_site):
    pass
        
class trap_site(job_site):
    pass

# Deliver more ore to hq (left side of the map) than your opponent. Use radars to find ore but beware of traps!

# height: size of the map
## --------- Function definitions ---------- ##
def release_site(x,y,sites,complete=True):
    for s in sites:
        if x == s.x and y == s.y:
            s.release(complete)
            
def flag_trap(x,y,ore_sites,radar_sites):
    for o in ore_sites:
        if x == o.x and y == o.y:
            o.trapped = True
    
    for r in radar_sites:
        if x == r.x and y == r.y:
            r.trapped = True
            
width, height = [int(i) for i in input().split()]
robot_list = []
ore_site_list = []
radar_site_list = [radar_site(7,3),
                   radar_site(7,11),
                   radar_site(11,7),
                   radar_site(14,3),
                   radar_site(14,11),
                   radar_site(23,3),
                   radar_site(23,11)]

'''trap_site_list = [trap_site(3,3),
                   trap_site(3,5),
                   trap_site(3,7),
                   trap_site(3,9),
                   trap_site(3,11),
                   trap_site(3,13)]'''
trap_site_list = []

first_turn = True  
radar_cooldown = 0
trap_cooldown = 0
            
# game loop
while True:
    # my_score: Amount of ore delivered
    my_score, opponent_score = [int(i) for i in input().split()]
    for j in range(height):
        inputs = input().split()
        for i in range(width):
            # ore: amount of ore or "?" if unknown
            # hole: 1 if cell has a hole
            ore = inputs[2*i]
            hole = int(inputs[2*i+1])
            if(ore != "?"):
                    #print("X:{},Y:{}\nOre?:{} Hole?:{}".format(i,j,int(ore),hole),file=sys.stderr)
                    exists = False
                    for o in ore_site_list:
                        if o.x == i and o.y == j:
                            exists = True
                            o.update(ore,hole)
                            break
                        else:
                            pass
                    if not exists:
                        ore_site_list.append(ore_site(i,j,ore,hole))
                        
    # entity_count: number of entities visible to you
    # radar_cooldown: turns left until a new radar can be requested
    # trap_cooldown: turns left until a new trap can be requested
    entity_count, radar_cooldown, trap_cooldown = [int(i) for i in input().split()]
    for i in range(entity_count):
        # entity_id: unique id of the entity
        # entity_type: 0 for your robot, 1 for other robot, 2 for radar, 3 for trap
        # y: position of the entity
        # item: if this entity is a robot, the item it is carrying (-1 for NONE, 2 for RADAR, 3 for TRAP, 4 for ORE)
        entity_id, entity_type, x, y, item = [int(j) for j in input().split()]
        if entity_type == 0 and first_turn:
            robot_list.append(robot(entity_id,x,y,item))
            
        elif entity_type == 0 and not first_turn:
            for r in robot_list:
                if r.bot_id == entity_id:
                    r.x = x
                    r.y = y
                    r.item = item
        
        elif entity_type == 3:
            flag_trap(x,y,ore_site_list,radar_site_list)
            
    for i in robot_list:
        for o in ore_site_list:
            o.distance(i.x,i.y)
            o.calc_score()
        for r in radar_site_list:
            r.distance(i.x,i.y)
            r.calc_score()
        for t in trap_site_list:
            t.distance(i.x,i.y)
            t.calc_score()
            
        ore_site_list.sort(key=lambda i: i.score, reverse = True)
        radar_site_list.sort(key=lambda i: i.score, reverse = True)
        trap_site_list.sort(key=lambda i: i.score, reverse = True)

        if i.x == 0:
            i.home = True
        else:
            i.home = False
            
            
        if i.job == "IDLE":
            successful = i.mine(ore_site_list)
            if not successful and not radar_cooldown:
                successful = i.survey(radar_site_list)
                if successful:
                    radar_cooldown = 7

            if not successful and not trap_cooldown:
                successful = i.trap(trap_site_list)
                if successful:
                    trap_cooldown = 7
        
        elif i.job == "MINER":
            if i.item == 4: # bot has ore
                i.timeout = 0
                if i.home == False:
                    release_site(i.dest_x,i.dest_y,ore_site_list)
                    i.set_destination(0,i.y)
                    i.job = "RETURNING"
                    i.action = "MOVE"
                else:
                    i.action = "WAIT"
            elif i.item == -1: # bot does not have ore
                if i.timeout > i.dig_delay:
                    release_site(i.dest_x,i.dest_y,ore_site_list)
                    i.job = "IDLE"
                    i.action = "WAIT"
                    i.timeout = 0
                    
                i.action = "DIG"
                i.timeout += 1
                    
        elif i.job == "SURVEYOR":
            if i.item == 2: # bot has radar
                i.radar_flag = True # flag that bot once had a radar
                i.set_destination(i.job_x, i.job_y)
                i.action = "DIG"
            elif i.item == -1: # bot does not have radar
                if not i.home and not i.radar_flag:
                    i.set_destination(0,i.y)
                    i.action = "MOVE"
                elif i.home and not i.radar_flag:
                    i.action = "REQUEST"
                elif i.item == -1 and i.radar_flag:
                    release_site(i.dest_x,i.dest_y,radar_site_list)
                    i.job = "IDLE"
                    i.action = "WAIT"
                
                else:
                    release_site(i.dest_x,i.dest_y,radar_site_list,complete=False)
                    i.job = "IDLE"
                    i.action = "WAIT"
                
            elif i.item == 4: # bot got ore when burying radar
                if i.home == False:
                    release_site(i.dest_x,i.dest_y,ore_site_list)
                    i.set_destination(0,i.y)
                    i.job = "RETURNING"
                    i.action = "MOVE"
                else:
                    i.action = "WAIT"
                    
        elif i.job == "TRAPPER":
            if i.item == 3: # bot has trap
                i.trap_flag = True # flag that bot once had a trap
                i.set_destination(i.job_x, i.job_y)
                i.action = "DIG"
            elif i.item == -1: # bot does not have trap
                if i.home == False and i.trap_flag == False:
                    i.set_destination(0,i.y)
                    i.action = "MOVE"
                elif i.home == True and i.radar_flag == False:
                    i.action = "REQUEST"
                else:
                    release_site(i.dest_x,i.dest_y,trap_site_list)
                    flag_trap(i.dest_x, i.dest_y,ore_site_list,radar_site_list)
                    i.job = "IDLE"
                    i.action = "WAIT"
                    
        elif i.job == "RETURNING":
            if not i.home:
                i.action = "MOVE"
            else:
                i.job = "IDLE"
        
        #print("R_cool: {} T_cool: {}".format(radar_cooldown, trap_cooldown),file=sys.stderr)
        i.speak()    
        i.act()
        first_turn = False
            
