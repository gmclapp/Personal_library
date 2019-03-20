'''It is recommended to use this package with the sanitize_inputs package.\n
The functions contained herein do not check for erroneous inputs.'''

__version__ = "0.2.6"

import math
import csv
import pandas as pd
import pdb
import os
from difflib import SequenceMatcher
import datetime as dt
import time

def dxdy(df, y_col, x_col):
    '''Given a dataframe and labels of an x and y column, This function
    returns the data frame with an additional column dx/dy that is the first
    derivative of x with respect to y.'''
    
    df_shifted = df.shift(1)
    df["dx/dy"] = (df[y_col]-df_shifted[y_col])/(df[x_col]-df_shifted[x_col])
    return(df)
    
def activate(x, k, epsilon=1):
    '''This function takes a value x, a trigger value k, and a smoothing factor
    epsilon and returns a number between 0 and 1 with an epsilon smoothed
    transition at x=k.'''

    y=math.tanh((x-k)/epsilon)/2+0.5
    return(y)

def deactivate(x, k, epsilon=1):
    '''This function takes a value x, a trigger value k, and a smoothing factor
    epsilon and returns a number between 0 and 1 with an epsilon smoothed
    transition at x=k.'''
    
    y=math.tanh((x-k)/epsilon)/-2+0.5
    return(y)

def timestamp():
    now = dt.datetime.fromtimestamp(time.time())
    sep=":"
    stamp = sep.join([str(now.year),
                      str(now.month),
                      str(now.day),
                      str(now.hour),
                      str(now.minute),
                      str(now.second)])
    return("["+stamp+"]")

def similar(a,b):
    return(SequenceMatcher(None,a,b).ratio())

def similar_dir(directory, desired, threshold=0.75):
    '''Takes the name of a desired subdirectory, and returns a directory that
    best matches the desired one with certainty above given threshold.'''
    candidates = []
    for f in os.listdir(directory):
        candidates.append((f, similar(f,desired)))

    candidates.sort(key=lambda x: x[1],reverse=True)
    best_match = candidates[0]
    if best_match[1] >= threshold:
        return(best_match[0])
    else:
        return(None)

def interpolate(x1,y1,x2,y2,x):
    '''This function returns a value, y, linearly interpolated using two x,y
    pairs of data and a given x between those pairs.'''
    
    try:
        y = ((y2-y1)/(x2-x1))*(x-x1) + y1
    except TypeError:
        y = y1
        
    return(y)

def interpolate_y(x1,y1,x2,y2,y):
    '''This function returns a value x, linearly interpolated using two x,y
    pairs of data and a given y between those pairs.'''

    try:
        m = (y2-y1)/(x2-x1)
        b = y1
        x = (y-b)/m
    except TypeError:
        x = x1

    return(x)

def tab_dict(rfile):
    '''This is a function that opens an excel file and returns a dictionary
    where the keys of the dictionary are the sheet names and the values are
    dataframes containing the data from the sheet. rfile must include the path
    if the file is not in the current working directory.'''

    try:
        xlsx = pd.ExcelFile(rfile)
        Sheet_frames = {sh:xlsx.parse(sh) for sh in xlsx.sheet_names}
        # This line creates a dictionary where the keys are the tab names,
        # and the values are the data from that tab.
        return(Sheet_frames)
    
    except FileNotFoundError:
        print(rfile,"Does not exist.")
        return(None)
           
def list_headers(rfile, r_c='r'):
    '''rfile is the csv file in which the data are stored. pass 'r' or 'c' for
    the second argument to indicate whether the headers are in the first row or
    the first column.'''
    
    headers = []
    RDR = csv.reader(open(rfile))
    if r_c.lower() == 'c':
        for row in RDR:
            print(row[0])
            headers.append(row[0])
                  
    elif r_c.lower() == 'r':
        headers = next(RDR)

    return(headers)

def vlookup(rfile, index, search_col, result_col,skip_headers=False):
    '''rfile is the name of file in which data are stored. index is the value
    to search database rows for. search_col is the column in which the
    index can be found. result_col should be the column from which the result
    should be extracted. This function is made to work smoothly with
    interpolate() Skip headers allows the user to skip searching the first row
    which will not happen automatically if the column labels are numbers.'''

    index = float(index)
    search_col = int(search_col)
    result_col = int(result_col)
    
    RDR = csv.reader(open(rfile,'r'), dialect = 'excel')
    pos_diff = math.inf 
    neg_diff = math.inf*-1

    x1 = None
    y1 = None
    x2 = None
    y2 = None

    for i, row in enumerate(RDR):
        # Search for the rows just smaller and just larger than the search
        # term. Calculate the difference between the x value in a given row
        # and the search term. Keep the rows that result in the smallest
        # positive difference and the smallest negative difference.
        if i == 0 and skip_headers:
            #next(RDR)
            print("Advanced a row")
            continue
        try:
            diff = index - float(row[search_col])
            
        except ValueError:
            if row[search_col] == "Inf":
                diff = math.inf
            continue

        if diff < pos_diff and diff > 0:
            x1 = float(row[search_col])
            y1 = float(row[result_col])
            pos_diff = diff

        elif diff > neg_diff and diff < 0:
            x2 = float(row[search_col])
            y2 = float(row[result_col])
            neg_diff = diff
            
        elif diff == 0:
            x1 = float(row[search_col])
            y1 = float(row[result_col])
            x2 = None
            y2 = None

    return (x1, y1, x2, y2)
    # Return the x,y pairs of the search column and result column just
    # above and below the desired x value.

def bernoulli_trial(n, k, p):
    '''Returns the probability between 0 and 1 of exactly k successes given
    n trials where the probability of success is p. k and n must be integers
    and p is a float between 0 and 1.'''
    
    q = 1-p
    binomial_coeff = math.factorial(n)/(math.factorial(k)*math.factorial(n-k))
    P = binomial_coeff*(p**k)*(q**(n-k))
    return(P)

def bernoulli_trial_n(k, p, P=0.95):
    '''Returns the sample size required to observe at least k successes if
    the probability of success in each trial is p to a confidence level of P.'''

    n = k # Sample size must be at least k in order to observe k successes.
    test_P = 0
    while test_P < P:
        test_P = 0
        for test_k in range(k, n-1):
            test_P += bernoulli_trial(n, test_k, p)
        n+= 1
        print("One can be {0:4.2f} confident that at least {1} successes will occur if {2} parts are tested.".format(test_P, k, n))
    return(n)
            
def favstats(rfile, column):
    '''This function calculates common statistical values for a given column
    of data found in the specified file.'''
    df = pd.read_csv(rfile)
    xbar = df[column].mean()
    sd = df[column].std()
    minimum = df[column].min()
    first = df[column].quantile(0.25) # first quartile
    median = df[column].median()
    third = df[column].quantile(0.75) # third quartile
    maximum = df[column].max()
    IQR = third - first

    print("Minimum: ", minimum,
          "\nFirst quartile: ", first,
          "\nMedian: ", median,
          "\nMean: ", xbar,
          "\nThird quartile: ",third,
          "\nMaximum: ", maximum,
          "\nStandard deviation: ",sd,
          "\nInter-quartile range: ",IQR,sep='')

def t_test_file(rfile, col, xbar=0, alpha=0.05, twotail=True, lower=True):
    '''One sample t-test. Arguments are the csv file in which the data are
    located and the column in which the data are found along with an alpha
    value. var is the column name in which the category of interest is stored.
    col is the column in which the response variable is stored. xbar is the
    variable to which the mean will be compared. twotail tells the function
    whether it should do a two tail test as opposed to a one tail test. lower
    is ignored for two tail, but determines which tail is considered in the one
    tail variant.'''
    
    df = pd.read_csv(rfile)

    # This line pulls data out of the data frame creating two new data frames
    # one for each label.

    # The resulting data structure is a tuple where element 0 is the group name
    # and element 1 is the actual sub-dataframe.
    xbar_test = df[col].mean()
    sd = df[col].std()
    n = len(df[col])
    DOF = n-1

    # Look up the appropriate t statistic - a 2 parameter interpolation function
    # would be nice here for an arbitrary value of alpha.
    if twotail:
        lookupfile = "twotail tstat.csv"
        
    else:
        lookupfile = "onetail tstat.csv"
    headers = list_headers(lookupfile,'r')
    for i, h in enumerate(headers):
        try:
            if float(h) == float(alpha):
                print("Alpha level is: ",float(alpha))
            else:
                pass
        except ValueError:
            continue
    x1,y1,x2,y2 = vlookup(lookupfile, DOF, 0, i,skip_headers=False)
    tsalpha = interpolate(x1,y1,x2,y2,DOF)

    std_err = sd/n**0.5

    # calculate the confidence interval
    diff = (xbar_test - xbar)
    upper = (diff) + tsalpha*std_err
    lower = (diff) - tsalpha*std_err
    print((1-float(alpha))*100,"% Confidence interval: ",lower," - ",upper,sep='')
    
    # calculate p-value
    ts = abs(diff/std_err)
    if twotail:
        #find p for given ts in twotail tstat.csv
        lookupfileT = ("twotail tstat Transpose.csv")
          
    else:
        #find p for given ts in onetail tstat.csv
        lookupfileT = ("twotail tstat Transpose.csv")
        if lower:
            pass
        else:
            pass
    headersT = list_headers(lookupfileT,'r')
    for i, h in enumerate(headersT):
        try:
            if float(h) == float(DOF):
                break
            else:
                pass
        except ValueError:
            continue   
    x1,y1,x2,y2 = vlookup(lookupfileT, ts, i, 0,skip_headers=True)
    print("({0},{1}) - ({2},{3})".format(x1,y1,x2,y2))
    print("avg: {0}\nsd: {1}\nn: {2}\ndiff: {3}\nstd_err: {4}"\
          .format(xbar_test,sd,n,diff,std_err))
    print("ts = {0}".format(ts))
    p = interpolate(x1,y1,x2,y2,ts)
    print("p = ",p)
    # formulate conclusion
    
def t_test2_file(rfile, var, c1, c2, treat, alpha=0.05, twotail=True, lower=True):
    '''Two sample t-test. Arguments are the csv file in which the data are
    located and the two columns to be compared along with an alpha value.
    var is the column name in which the categories are stored, c1 and c2 are
    the two labels in that column to be compared. treat is the treatment
    varible. ie the variable that will be used to compare the groups. twotail
    tells the function whether it should do a two tail test as opposed to a one
    tail test. lower is ignored for two tail, but determines which tail is
    considered in the one tail variant.'''

    df = pd.read_csv(rfile)
    groups = dict((x,y) for x,y in df.groupby(var))

    # This line pulls data out of the data frame creating two new data frames
    # one for each label.

    # The resulting data structure is a tuple where element 0 is the group name
    # and element 1 is the actual sub-dataframe.
    xbar1 = groups[c1][treat].mean()
    xbar2 = groups[c2][treat].mean()

    # Pandas standard deviation function uses Bessel's correction by default.
    s1 = groups[c1][treat].std()
    s2 = groups[c2][treat].std()

    n1 = len(groups[c1][treat])
    n2 = len(groups[c2][treat])
    n = min(n1,n2)
    DOF = n-1
    # n will be used to calculate the standard error. Choosing the smaller of
    # the two sample sizes yields a conservative estimate.
    
    # Calculate the pooled standard deviation
    sp = (((n1-1)*s1**2+(n2-1)*s2**2)/(n1+n2-2))**0.5
    
    # Look up the appropriate t statistic - a 2 parameter interpolation function
    # would be nice here for an arbitrary value of alpha.
    if twotail:
        lookupfile = "twotail tstat.csv"
        
    else:
        lookupfile = "onetail tstat.csv"
    headers = list_headers(lookupfile,'r')
    for i, h in enumerate(headers):
        try:
            if float(h) == float(alpha):
                break
            else:
                pass
        except ValueError:
            continue   
    x1,y1,x2,y2 = vlookup(lookupfile, DOF, 0, i,skip_headers=True)
    print("DOF: {}\ni: {}".format(DOF,i))
    tsalpha = interpolate(x1,y1,x2,y2,DOF)
    # There is an issue here where if a sample size n=2, DOF=1 and the lookup
    # table returns a nonetype

    std_err = sp/n**0.5

    # calculate the confidence interval
    diff = (xbar1 - xbar2)
    upper = (diff) + tsalpha*std_err
    lower = (diff) - tsalpha*std_err
    
    # calculate p-value
    ts = abs(diff/std_err)
    if twotail:
        #find p for given ts in twotail tstat.csv
        lookupfileT = ("twotail tstat Transpose.csv")
          
    else:
        #find p for given ts in onetail tstat.csv
        lookupfileT = ("twotail tstat Transpose.csv")
        if lower:
            pass
        else:
            pass
    headersT = list_headers(lookupfileT,'r')
    for i, h in enumerate(headersT):
        try:
            if float(h) == float(DOF):
                break
            else:
                pass
        except ValueError:
            continue   
    x1,y1,x2,y2 = vlookup(lookupfileT, ts, i, 0,skip_headers=True)
    print("x1,y1,x2,y2",x1,y1,x2,y2)
    p = interpolate(x1,y1,x2,y2,ts)
    # formulate conclusion

    print("xbar1 = ",xbar1,
          "\nxbar2 = ",xbar2,
          "\ns1 = ",s1,
          "\ns2 = ",s2,
          "\nn1 = ",n1,
          "\nn2 = ",n2,
          "\nn = ",n,
          "\nsp = ",sp,
          "\ntsalpha = ",tsalpha,
          "\nts = ",ts,
          "\ndiff = ",diff,
          "\nupper = ",upper,
          "\nlower = ",lower,
          "\nstd_err = ",std_err,
          "\np = ",p,sep='')
    
    return(df)

def paired_t_test(DF1, DF2, alpha=0.05, mu=0, twotail=True, lower=True):
    '''This function takes two pandas dataframes which must have the same index
    and find the change in each item and perform a t-test to compare the
    change to a given number.
    
    Index entries which don't appear in both dataframes will be removed
    automatically.'''

    diffDF = pd.DataFrame()
    for col in DF1:
        try:
            diffDF[col] = DF1[col].sub(DF2[col])
        except:
            print("Paired data can only be calculated for numeric data.")
            continue

    diffDF = diffDF.dropna()
    print(diffDF)
    p = t_test(diffDF, alpha, mu, twotail, lower)
    return(p)

def t_test(series, alpha=0.05, mu=0, twotail=True, lower=True):
    '''This function performs a 1 sample t-test on a pandas data series rather
    than a file.'''

    xbar_test = series.mean()
    sd = series.std()
    n = len(series)
    DOF = n-1

    # Look up the appropriate t statistic - a 2 parameter interpolation function
    # would be nice here for an arbitrary value of alpha.
    if twotail:
        lookupfile = "twotail tstat.csv"
        
    else:
        lookupfile = "onetail tstat.csv"
    headers = list_headers(lookupfile,'r')
    for i, h in enumerate(headers):
        try:
            if float(h) == float(alpha):
                print("Alpha level is: ",float(alpha))
            else:
                pass
        except ValueError:
            continue
    x1,y1,x2,y2 = vlookup(lookupfile, DOF, 0, i,skip_headers=False)
    tsalpha = interpolate(x1,y1,x2,y2,DOF)

    std_err = sd/n**0.5

    # calculate the confidence interval
    diff = (xbar_test - mu)
    upper = (diff) + tsalpha*std_err
    lower = (diff) - tsalpha*std_err
    print((1-float(alpha))*100,"% Confidence interval: ",lower," - ",upper,sep='')
    
    # calculate p-value
    ts = abs(diff/std_err)
    if twotail:
        #find p for given ts in twotail tstat.csv
        lookupfileT = ("twotail tstat Transpose.csv")
          
    else:
        #find p for given ts in onetail tstat.csv
        lookupfileT = ("twotail tstat Transpose.csv")
        if lower:
            pass
        else:
            pass
    headersT = list_headers(lookupfileT,'r')
    for i, h in enumerate(headersT):
        try:
            if float(h) == float(DOF):
                break
            else:
                pass
        except ValueError:
            continue   
    x1,y1,x2,y2 = vlookup(lookupfileT, ts, i, 0,skip_headers=True)
    print("({0},{1}) - ({2},{3})".format(x1,y1,x2,y2))
    print("avg: {0}\nsd: {1}\nn: {2}\ndiff: {3}\nstd_err: {4}"\
          .format(xbar_test,sd,n,diff,std_err))
    print("ts = {0}".format(ts))
    p = interpolate(x1,y1,x2,y2,ts)
    print("p = ",p)

    return(p)
    
def r_ch_arc(Arc, Chord, dr):
    '''Find the radius of a circle given a chord length and an arc length. This
    is a numerical solution. The argument dr is the desired level of
    precision.'''
    
    a = float(Arc)
    c = float(Chord)
    dr = float(dr)
    
    radius = 0
    error = 100
    # numberical solution for radius. Iterates until error is less than
    # specified dr.
    while (error > dr):
        radius += dr
        
        tempA = math.sin(a/(2*radius))
        tempB = c/(2*radius)
        error = abs(tempA-tempB)

    return(radius)
    
