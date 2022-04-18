#import pymatrix
import random
import time
import csv

random.seed()

import pygame, sys #imports the pygame and sys modules
from pygame.locals import * #pygame.locals has the constants like QUIT, MOUSEMOTION, AND K_ESCAPE.

pygame.init()#This must be called before any other pygame code.
fpsClock = pygame.time.Clock() #The Clock object makes sure our program runs (at most) at a certain FPS.

screen_height = 480
screen_width = 480
scrn_bckgrnd = (125, 125, 125) #grey
msg_color = (255, 255, 255) #white
screen = pygame.display.set_mode((screen_width,screen_height)) #set_mode() creates the window. Param is (width, height) in pixels. The Surface object returned is drawn to the screen when pygame.display.update() is called.
pygame.display.set_caption('Doods')

mousex, mousey = 0,0

fontObj = pygame.font.Font('freesansbold.ttf', 24) #Create a Font object with a font of size 32 points
msg = ' '

max_dudes = 75
data = csv.writer(open('data.csv','w'))


class neuron:
    def __init__(self, name, excitation, saturation, decayrate):
        self.excite = excitation #Current excitation level
        self.sat = saturation    #Excitation level required to fire
        self.decay = decayrate   #Amount excitation falls per tick, min = 0

class allele:
    def __init__(self, attr, dom, val):
        self.attr = attr #This describes the attribute the allele affects
        self.dom = dom   #This describes how dominant the allele is
        self.val = val   #This describes the value of the allele

class gene:
    def __init__(self, allele1, allele2):
        self.attr = allele1.attr
        #The following lines insure that the more dominant allele is represented
        #by a1, which will be the expressed allele.
        if allele1.dom > allele2.dom:
            self.a1 = allele1
            self.a2 = allele2
        else:
            self.a2 = allele1
            self.a1 = allele2

    def printstats(self):
        data.writerow([str(self.attr), str(self.a1.dom), str(self.a1.val)])
        #print("Attribute:",self.attr,"allele 1 dominance:",self.a1.dom,"value:",self.a1.val)
        #print("Attribute:",self.attr,"allele 2 dominance:",self.a2.dom,"value:",self.a2.val)

class doodlist:
    def __init__(self):
        self.master = []
        self.live = []
        self.dead = []
        
    def add_dood(self, parents = False, parent1 = None, parent2 = None):
        if len(self.live) < max_dudes:
            if parents == False:
                newdood = dood(len(self.master))
                
            else:
                for d in self.live:
                    if d.num == parent1:
                        #print("Found parent 1.")
                        temp1 = d
                    elif d.num == parent2:
                        #print("Found parent 2.")
                        temp2 = d
                    else:
                        pass
                        #print("Not a match.")
                cell1 = temp1.build_crossover_cell()
                cell2 = temp2.build_crossover_cell()
                newdood = dood(len(self.master), True, parent1, parent2, cell1, cell2)
            self.master.append(newdood)
            self.live.append(newdood)
        
    def kill_dood(self, dood_num):
        for index in range(len(self.live)-1):
            if self.live[index].num == dood_num:
                self.live[index].alive = False
                self.dead.append(self.live[index])
                self.live.pop(index)

    def data_dump(self):
        for d in self.live:
            pass
            #Write an algorithm that averages the value of each attribute and then prints it beneath the
            #appropriate header.
                
class dood:
    def __init__(self, num, parents = False, parent1=None, parent2=None, cell1 = None, cell2 = None):

        #dood identifiers
        self.num = num
        self.gen = 0
        self.ref_epoch = time.time() #time in seconds that the refactory period was set.
        self.parent1 = parent1 #Num value of 1st parent
        self.parent2 = parent2 #Num value of 2nd parent
        
        #allele description, dominance, allele value
        self.dna = []
        if parents == False:
            R1 = allele("Red", random.randint(0,255), random.randint(0,255))
            R2 = allele("Red", random.randint(0,255), random.randint(0,255))
            self.dna.append(gene(R1,R2))
            G1 = allele("Green", random.randint(0,255), random.randint(0,255))
            G2 = allele("Green", random.randint(0,255), random.randint(0,255))
            self.dna.append(gene(G1,G2))
            B1 = allele("Blue", random.randint(0,255), random.randint(0,255))
            B2 = allele("Blue", random.randint(0,255), random.randint(0,255))
            self.dna.append(gene(B1,B2))
            S1 = allele("Size", random.randint(0,255), random.randint(0,255))
            S2 = allele("Size", random.randint(0,255), random.randint(0,255))
            self.dna.append(gene(S1,S2))
            GR1 = allele("Growth rate", random.randint(0,255), random.randint(0,255))
            GR2 = allele("Growth rate", random.randint(0,255), random.randint(0,255))
            self.dna.append(gene(GR1, GR2))
            Ref1 = allele("Refactory period", random.randint(0,255), random.randint(0,255))
            Ref2 = allele("Refactory period", random.randint(0,255), random.randint(0,255))
            self.dna.append(gene(Ref1, Ref2))
            mut1 = allele("Mutation chance", random.randint(0,255), random.randint(0,255))
            mut2 = allele("Mutation chance", random.randint(0,255), random.randint(0,255))
            self.dna.append(gene(mut1, mut2))
            ms1 = allele("Max size", random.randint(0,255), random.randint(0,255))
            ms2 = allele("Max size", random.randint(0,255), random.randint(0,255))
            self.dna.append(gene(ms1, ms2))
            
        else:
            for index in range(len(cell1)):
                self.dna.append(gene(cell1[index], cell2[index]))
                
                
            
        #gene expression
        self.red = self.dna[0].a1.val
        self.green = self.dna[1].a1.val
        self.blue = self.dna[2].a1.val
        self.size = self.dna[3].a1.val/25.5
        self.draw_size = int(self.size)
        self.growth_rate = self.dna[4].a1.val/2550.
        self.ref_per = self.dna[5].a1.val * 0.0588 + 5 #refactory period between 30 and 330 seconds
        self.mutation_chance = self.dna[6].a1.val / 255
        self.max_size = self.dna[7].a1.val + self.size + 1
        
        #initial position
        self.x = random.randint(0,screen_width)
        self.y = random.randint(0,screen_height)

        self.heading = random.randint(0,359)
        #initial velocity
        self.vx = random.randint(-5, 5)
        self.vy = random.randint(-5, 5)
        if self.vx == 0:
            self.vx == 1
        if self.vy == 0:
            self.vy = 1

        #dood status indicators
        self.alive = True

        #neuro network

    def gene_expression(self, desc1, desc2):
        for allele in self.dna:
            if allele[0] == desc1:
                temp1 = allele
            elif allele[0] == desc2:
                temp2 = allele
        if temp1[1] > temp2[1]:
            result = temp1[2]
        else:
            result = temp2[2]
        return(result)

    def build_crossover_cell(self):
        cell = []
        for gene in self.dna:
            #choosing a temp value of either 1 or 0 gives each allele a
            #50% chance of being selected. a crossover cell is built with
            #one allele from each gene in a dood's dna
            temp = random.randint(0,1)
            mutation_roll = random.random() #Pray to RNGesus to see if the gene mutates
            if mutation_roll < self.mutation_chance: #allele will mutate because mutation roll is lower than mutation chance
                up_down = random.randint(0,1) #determine whether the given gene is going to go up or down
                att_dom = random.randint(0,1) #determine whether the attribute value or the dominance value is affected
                if temp: #allele 1 is selected
                    if att_dom: #attribute is affected
                        if up_down: #allele is modified up
                            temp_allele = allele(gene.a1.attr, gene.a1.dom, gene.a1.val +1)
                        else: #allele is modified down
                            temp_allele = allele(gene.a1.attr, gene.a1.dom, gene.a1.val -1)
                    else: #dominance is affected
                        if up_down: #allele is modified up
                            temp_allele = allele(gene.a1.attr, gene.a1.dom+1, gene.a1.val)
                        else: #allele is modified down
                            temp_allele = allele(gene.a1.attr, gene.a1.dom-1, gene.a1.val)
                else: #allele 2 is selected
                    if att_dom: #attribute is affected
                        if up_down: #allele is modified up
                            temp_allele = allele(gene.a2.attr, gene.a2.dom, gene.a2.val +1)
                        else: #allele is modified down
                            temp_allele = allele(gene.a2.attr, gene.a2.dom, gene.a2.val -1)
                    else: #dominance is affected
                        if up_down: #allele is modified up
                            temp_allele = allele(gene.a2.attr, gene.a2.dom+1, gene.a2.val)
                        else: #allele is modified down
                            temp_allele = allele(gene.a2.attr, gene.a2.dom-1, gene.a2.val)

                if temp_allele.dom < 0:
                    temp_allele.dom = 0
                if temp_allele.dom > 255:
                    temp_allele.dom = 255
                if temp_allele.val < 0:
                    temp_allele.val = 0
                if temp_allele.val > 255:
                    temp_allele.val = 255
                    
                cell.append(temp_allele)
            else: #cell will not mutate                
                if temp:
                    cell.append(gene.a1)
                else:
                    cell.append(gene.a2)

        return(cell)
            
    def printstats(self):
        print("I'm dood #:", self.num)
        print("RGB:",self.red,self.green,self.blue)
        for gene in self.dna:
            gene.printstats()
            
    def update(self):
        self.size += self.growth_rate
        if self.size > self.max_size:
            self.size = self.max_size
        self.draw_size = int(self.size)
        
        self.x += self.vx
        self.y += self.vy
        if (self.x - self.size) < 0 or (self.x + self.size) > screen_width:
            self.vx = self.vx * -1
            self.x += self.vx
        if (self.y - self.size) < 0 or (self.y + self.size) > screen_height:
            self.vy = self.vy * -1
            self.y += self.vy
        
    def draw_dood(self, surf):
        try:
            pygame.draw.circle(surf, (self.red, self.green, self.blue), (int(self.x), int(self.y)), self.draw_size)
        except TypeError:
            print("R:", self.red, "G:", self.green, "B:", self.blue, "x:",
                  self.x, "y:", self.y, "size:", self.draw_size)

def test_ref_period(dood1, dood2):
    if (int(time.time() - dood1.ref_epoch) >= int(dood1.ref_per)) and (int(time.time() - dood2.ref_epoch) >= int(dood2.ref_per)):
        doodgroup.add_dood(parents = True, parent1 = dood1.num, parent2 = dood2.num)
        dood1.ref_epoch = time.time()
        dood2.ref_epoch = time.time()
        
    else:
        pass
    
doodgroup = doodlist()


while(True):     

    screen.fill(scrn_bckgrnd) #This will fill the Surface object with background color specified above

    msgBox = fontObj.render(msg, False, msg_color) #render() creates a surface object with the text drawn on it in the specified font and color. You can blit() this Surface object to the window's Surface object.
    screen.blit(msgBox, (0,0))

    for event in pygame.event.get(): #pygame.event.get() returns a list of all Event objects that happened since the last time get() was called
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION: #The event object has type, pos, key and other attributes depending on the type of event it is.
            mousex, mousey = event.pos
            temp = ('X: %.3f, Y: %.3f' %(mousex, mousey))
            msg = temp
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            if event.button == 1:
                msg = 'Left mouse click'
                mouse1_flag = 1
            if event.button == 3:
                msg = 'Right mouse click'
                mouse2_flag = 1
        elif event.type == MOUSEBUTTONUP:
            mousex, mousey = event.pos
            if event.button == 1:
                if mouse1_flag == 1:
                    doodgroup.add_dood()
                    msg = 'Dood created'
                    mouse1_flag = 0
                else:
                    pass
            if event.button == 3:
                if mouse2_flag == 1:
                    msg = 'Kill dood.'
                    for d in doodgroup.live:
                        temp_dist = (mousex - d.x)**2 + (mousey - d.y)**2
                        if temp_dist <= d.size**2:
                            doodgroup.kill_dood(d.num)
                        d.printstats()
                    mouse2_flag = 0
                else:
                    pass
                
            elif event.button == 2:
                msg = 'middle mouse click'
            elif event.button == 4:
                msg = 'Mouse scrolled up.'
            elif event.button == 5:
                msg = 'Mouse scrolled down.'
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    for d in doodgroup.live:
        d.update()
        d.draw_dood(screen)
        for d2 in doodgroup.live:
            if d.num != d2.num:
                col_dist = (d.x-d2.x)**2 + (d.y-d2.y)**2
                if col_dist <= (d.size + d2.size)**2:
                    test_ref_period(d, d2)
                    
    pygame.display.update() #The window is not drawn to the actual screen until pygame.display.update is called.
    fpsClock.tick(30) #wait long enough to run at 30 frames per second. (Call this after pygame.display.update().)
  
