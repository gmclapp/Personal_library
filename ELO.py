import sanitize_inputs as si
import time

class player():
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.S = 0

    def reset_S(self):
        self.S = 0
        
    def get_Q(self, D=400):
        self.Q = 10**(self.rating/D)
        return(self.Q)

    def get_E(self, Qsum):
        self.E = self.Q/Qsum
        return(self.E)

    def update_rating(self, N=1, K=16):
        self.rating += K*(self.S - (self.E*N))


def ELOgame(players, D=400, K=16):
    '''Takes a list of tuples. (player name, rating) and performs operations
    on ELO ratings.'''
    num_players = len(players)
    player_list = []
    name_list = []
    for p in players:
        player_list.append(player(p[0],p[1]))
        name_list.append(p[0])

    games = si.get_integer("How many games were played? ")
    
    if games == 1:
        print("Who won?\n")
        winner = name_list[si.select(name_list)]
        for p in player_list:
            if p.name == winner:
                p.S += 1
            else:
                pass
    else:
        for game in range(games):
            print("Who won game {}? ".format(game+1))
            winner = name_list[si.select(name_list)]
            for p in player_list:
                if p.name == winner:
                    p.S += 1
                else:
                    pass

    Qsum = 0
    for p in player_list:
        Qsum += p.get_Q(D)

    for p in player_list:
        p.get_E(Qsum)
        p.update_rating(N=games)
        print("Player: {} {:<4.0f}".format(p.name,p.rating))
        
        
        
players = (("Glenn",932),("Jeff",823))

ELOgame(players, D=800, K=32)
time.sleep(30)
