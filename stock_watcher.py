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

df.plot('Adj Close')
plt.show()
