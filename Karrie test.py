import random

Parent_pool = ["PP","Pp"]

A = "Pp" # We know the genetic makeup of one parent

children = []
for i in range (100000):
    B = random.choice(Parent_pool)
    Aallele = A[random.randrange(0,2)]
    Ballele = B[random.randrange(0,2)]
    C=Aallele+Ballele
    if C != "pp": # We have evidence that shows the child cannot be "pp"
        children.append(C)

PPcount = 0
Ppcount = 0

for child in children:
    if child == "Pp" or child == "pP":
        Ppcount += 1
    elif child == "PP":
        PPcount += 1
    else:
        print("An unexpected mutant")

PP_proportion = PPcount/len(children)
Pp_proportion = Ppcount/len(children)

print("PP_proportion: {}, Pp_proporiton: {}".format(PP_proportion,Pp_proportion))

