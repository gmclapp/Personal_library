def V1(r, h):
    V = (4/3*math.pi*r**3) + (math.pi*h*r**2)
    return (V)

def V2 (P1,P2,r,h):
    V = P1*math.pi*r**2*(4/3*r+h)/P2
    return(V)

import math
import sanitize_inputs as si

print(V1(6,32))
P1 = 14.7
P2 = si.get_real_number("Enter absolute working pressure of expansion tank (psi)\n>>> ",
                  lower=0)
print(V2(P1,P2,6,32))
