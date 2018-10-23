'''It is recommended to use this package with the sanitize_inputs package as the
functions contained herein do not check for erroneous inputs.'''

import math

def bernoulli_trial(n, k, p):
    '''Returns the probability between 0 and 1 of exactly k successes given
    n trials where the probability of success is p. k and n must be integers
    and p is a float between 0 and 1.'''
    
    q = 1-p
    binomial_coeff = math.factorial(n)/(math.factorial(k)*math.factorial(n-k))
    P = binomial_coeff*(p**k)*(q**(n-k))
    return(P)

def r_ch_arc(Arc, Chord, dr):
    '''Find the radius of a circle given a chord length and an arc length. This
    is a numerical solution. The argument dr is the desired level of
    precision.'''
    
    a = float(Arc)
    c = float(Chord)
    dr = float(dr)
    
    radius = 0
    error = 100
    while (error > dr):
        radius += dr
        
        tempA = math.sin(a/(2*radius))
        tempB = c/(2*radius)
        error = abs(tempA-tempB)

    return(radius)
    
