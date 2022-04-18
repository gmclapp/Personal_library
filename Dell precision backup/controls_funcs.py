import math
e = math.e
PI = math.pi

def compensator(wmax, phimax):
#returns the parameters of a lead or lag compensator transfer function Td and alpha
#given the max phase desired at the frequency desired
    alpha = (1-math.sin(math.radians(phimax)))/(1+math.sin(math.radians(phimax)))
    Td = 1/(wmax*alpha**0.5)
    print("alpha",alpha)
    print("Td",Td)
    print("alpha*Td:",alpha*Td,"\n\n")
    return(alpha, Td)

def zeta(PO):
    z = abs(math.log(PO,e))/(PI**2+math.log(PO,e)**2)**0.5
    return(z)

def wn(ts, zeta):
    w = 4.6/(zeta*ts)
    print("If ts is minimum, wn is minimum")
    return w
