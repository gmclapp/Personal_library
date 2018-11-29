import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import json
import sys
import sanitize_inputs as si

__version__ = '0.2.0'

class positions():
    def __init__(self):
        self.position_list = []

    def list_positions(self):
        plist = []
        for pos in self.position_list:
            plist.append(pos['ticker'])
        return(plist)
    
    def enter_order(self, buysell, date, ticker, shares, price, commission=4.95, fees=0):
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
        print("Calculating cost basis...")
        for pos in self.position_list:
            accum = 0
            shares = 0
            for transaction in pos['transactions']:
                if transaction['b/s'] == 'b':
                    shares += transaction['shares']
                    accum += transaction['price']*transaction['shares'] + transaction['commission'] + transaction['fees']
                elif transaction['b/s'] == 's':
                    shares -= transaction['shares']
                    accum -= transaction['price']*transaction['shares'] + transaction['commission'] + transaction['fees']

            try:        
                pos['cost basis'] = accum/shares
            except ZeroDivisionError:
                print("Currently holding zero shares.")
                pos['cost basis'] = 0
            pos['current shares'] = shares

    def save_positions(self):
        with open("watchlist.stk",'w') as f:
            json.dump(self.position_list, f)

    def load_positions(self):
        print("Loading trading data...")
        with open("watchlist.stk","r") as f:
            self.position_list = json.load(f)

def order(watch_list):
    today = dt.date.today()
    orders = ['Buy',
              'Sell']
    date_options = ['Today',
                    'Enter date']
    print("What kind of order?")

    order = orders[si.select(orders)]
    print("When was this order?")
    date_selection = date_options[si.select(date_options)]
    if date_selection == 'Today':
        date = today
    elif date_selection == 'Enter date':
        year = si.get_integer("Enter year.\n>>>",upper=today.year+1,lower=1970)
        month = si.get_integer("Enter month.\n>>>",upper=13,lower=0)
        day = si.get_integer("Enter day.\n>>>",upper=32,lower=0)
        date_str = str(year)+'-'+str(month)+'-'+str(day)
        
    tick = input("Enter stock ticker.\n>>>").upper()
    shares = si.get_integer("Enter number of shares.\n>>>",lower=0)
    price = si.get_real_number("Enter share price.\n>>>",lower=0)
    comm = si.get_real_number("Enter commission.\n>>>",lower=-0.0001)
    fee = si.get_real_number("Enter fees.\n>>>",lower=-0.0001)
    
    if order == 'Buy':
        watch_list.enter_order('b', date_str, tick, shares, price, comm, fee)
    elif order == 'Sell':
        watch_list.enter_order('s', date_str, tick, shares, price, comm, fee)

def view(pos):
    print("Ticker: {}".format(pos["ticker"]))
    print("Shares: {}".format(pos["current shares"]))
    print("Current cost basis: ${:<7.2f}".format(pos["cost basis"]))
    today = dt.date.today()
    df = web.DataReader(pos["ticker"],"yahoo",today)
    last_close = df["Close"][0]
    print("Current price: ${:<7.2f}\n".format(last_close))
    for t in pos["transactions"]:
        print("{}: {} {} @ ${:<7.4f}".format(t['date'],t['b/s'].upper(),t['shares'],t['price']))
    print("\n",end='')
    
watch_list = positions()

style.use("fivethirtyeight")

print('\033[2J')
watch_list.load_positions()
watch_list.calc_cost_basis()

while(True):
    try:
        selections = ['Order','View','Clear console','Quit']
        selection = selections[si.select(selections)]
        if selection == 'Order':
            order(watch_list)
        elif selection == 'View':
            print("\n",end='')# Add whitespace between this and previous menu.
            viewlist = watch_list.list_positions()
            view_pos = viewlist[si.select(viewlist)]
            for pos in watch_list.position_list:
                if pos["ticker"] == view_pos:
                    view(pos)
                else:
                    pass
        elif selection == 'Clear console':
            print('\033[2J')
            # console command to clear console and return to (0,0)
        elif selection == 'Quit':
            print("Save changes?")
            yn = ['Yes','No']
            sav = yn[si.select(yn)]
            if sav == 'Yes':
                watch_list.save_positions()
            else:
                pass
            break
    except:
        print("Unexpected error:",sys.exc_info())
        continue
    
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
