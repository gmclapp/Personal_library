'''It is recommended to use this package with the sanitize_inputs package as the
functions contained herein do not check for erroneous inputs.'''

def bernoulli_trial(n, k, p):
    '''Returns the probability between 0 and 1 of exactly k successes given
    n trials where the probability of success is p. k and n must be integers
    and p is a float between 0 and 1.'''

    import math
    
    q = 1-p
    binomial_coeff = math.factorial(n)/(math.factorial(k)*math.factorial(n-k))
    P = binomial_coeff*(p**k)*(q**(n-k))
    return(P)

    
    
