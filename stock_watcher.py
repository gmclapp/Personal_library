import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import csv

class positions():
    def __init__(self):
        self.position_list = []
        
    def enter_order(self, buysell, date, ticker, shares, price, commission, fees=0):
        '''buysell = 'buy' or 'sell', date of order, stock ticker (not case
        sensitive), price of order, number of shares transacted,
        commission, and fees if applicable.'''
        exists_flag = False
        ticker = ticker.upper()
        for pos in self.position_list:
            if ticker == pos['ticker']:
                exists_flag = True
                print("Position is already on watch list")
                pos['transactions'].append({'b/s':buysell,'date':date,'price':price,'commission':commission,'fees':fees,'shares':shares})
        if exists_flag:
            pass
        else:
            self.position_list.append({'ticker':ticker,
                                       'transactions':[{'b/s':buysell,'date':date,'price':price,'commission':commission,'fees':fees,'shares':shares}],
                                       'dividends':[],
                                       'cost basis':shares*price + commission + fees,
                                       'current shares':shares})
    def enter_ticker(self, ticker):
        self.position_list.append({'ticker':ticker,
                                   'transactions':[],
                                   'dividends':[],
                                   'cost basis':0,
                                   'current shares':0})
    def calc_cost_basis(self):
        self.calc_num_shares()
        for pos in self.position_list:
            accum = 0
            for transaction in pos['transactions']:
                if transaction['b/s'] == 'b':
                    accum -= transaction['price']*transaction['shares'] - transaction['commission'] - transaction['fees']
                elif transaction['b/s'] == 's':
                    accum += (transaction['price']*transaction['shares'] - transaction['commission'] - transaction['fees'])
                    
            pos['cost basis'] = accum
    def calc_num_shares(self):
        pass
        
watchlist_file = csv.reader(open("watchlist.csv",'r'),dialect='excel')
watch_list = positions()

quotes = []

style.use("fivethirtyeight")
start = dt.datetime(2017,4,1)
today = dt.datetime(2018,10,28)


df = web.DataReader("TSLA","yahoo",start,today)
##print(df.head(10)) # The argument is the number of rows head returns
##print(df.tail(10)) # This does the same as head but returns rows from the end of the dataframe

##-example data structure-##
##positions = 
##[{'ticker':'GM',
## 'transactions':[{'b/s':'buy','date':'01-Nov-2018','price':35.50,'commission':4.95,'fees':0.00,'shares':15},
##                 {'b/s':'sell','date':'05-Nov-2018','price':36.25,'commission':4.95,'fees':0.00,'shares':15},
##                 {'b/s':'buy','date':'06-Nov-2018','price':32.25,'commission':4.95,'fees':0.00,'shares':15}],
## 'dividends':[{'date':'02-Nov-2018','amount':0.15,'shares':15},
##              {'date':'25-Nov-2018','amount':0.12,'shares':15}],
## 'cost basis':32.22,
##  'current shares':15},
## {'ticker':'F',
## 'transactions':[{'b/s':'buy','date':'01-Oct-2018','price':12.40,'commission':4.95,'fees':0.00,'shares':100},
##                 {'b/s':'sell','date':'05-Oct-2018','price':13.10,'commission':4.95,'fees':0.00,'shares':70},
##                 {'b/s':'buy','date':'06-Nov-2018','price':9.15,'commission':4.95,'fees':0.00,'shares':200}],
## 'dividends':[{'date':'02-Oct-2018','amount':0.07,'shares':100},
##              {'date':'25-Nov-2018','amount':0.11,'shares':230}],
## 'cost basis':9.285,
##  'current shares':230}]
