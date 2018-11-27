import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import csv

watchlist_file = csv.reader(open("watchlist.csv",'r'),dialect='excel')
watch_list = []
for line in watchlist_file:
    watch_list.append(line[0])

quotes = []

style.use("fivethirtyeight")
start = dt.datetime(2017,4,1)
today = dt.datetime(2018,10,28)


df = web.DataReader("TSLA","yahoo",start,today)
##print(df.head(10)) # The argument is the number of rows head returns
##print(df.tail(10)) # This does the same as head but returns rows from the end of the dataframe

##-example data structure-##
positions = 
[{'ticker':'GM',
 'transactions':[{'b/s':'buy','date':'01-Nov-2018','price':35.50,'commission':4.95,'fees':0.00,'shares':15},
                 {'b/s':'sell','date':'05-Nov-2018','price':36.25,'commission':4.95,'fees':0.00,'shares':15},
                 {'b/s':'buy','date':'06-Nov-2018','price':32.25,'commission':4.95,'fees':0.00,'shares':15}],
 'dividends':[{'date':'02-Nov-2018','amount':0.15,'shares':15},
              {'date':'25-Nov-2018','amount':0.12,'shares':15}],
 'cost basis':32.22},
 {'ticker':'F',
 'transactions':[{'b/s':'buy','date':'01-Oct-2018','price':12.40,'commission':4.95,'fees':0.00,'shares':100},
                 {'b/s':'sell','date':'05-Oct-2018','price':13.10,'commission':4.95,'fees':0.00,'shares':70},
                 {'b/s':'buy','date':'06-Nov-2018','price':9.15,'commission':4.95,'fees':0.00,'shares':200}],
 'dividends':[{'date':'02-Oct-2018','amount':0.07,'shares':100},
              {'date':'25-Nov-2018','amount':0.11,'shares':230}],
 'cost basis':9.285}]
