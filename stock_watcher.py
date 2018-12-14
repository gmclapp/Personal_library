import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import json
import sys
import sanitize_inputs as si

__version__ = '0.5.0'


class positions():
    def __init__(self):
        self.position_list = []

    def list_positions(self):
        plist = []
        for pos in self.position_list:
            plist.append(pos['ticker'])
        return(plist)
    
    def enter_order(self, buysell, date, ticker, shares, price, commission=4.95, fees=0):
        '''buysell = 'buy' or 'sell', date of order(str), stock ticker (not case
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

    def enter_dividend(self, ticker, date, amount, shares):
        exists_flag = False
        ticker = ticker.upper()
        for pos in self.position_list:
            if ticker == pos['ticker']:
                exists_flag = True
                total = amount*shares
                print("Shares: {}; Dividend: ${:<7.2f}; Total: ${:<7.2f}".format(shares,amount,total))
                pos['dividends'].append({'date': date,
                                         'amount':amount,
                                         'shares':shares,
                                         'total':total})

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
                    accum += transaction['price']*transaction['shares']\
                             + transaction['commission'] + transaction['fees']
                elif transaction['b/s'] == 's':
                    shares -= transaction['shares']
                    accum -= transaction['price']*transaction['shares']\
                             + transaction['commission'] + transaction['fees']
            for d in pos['dividends']:
                accum -= d['total']
                    

            try:        
                pos['cost basis'] = accum/shares
            except ZeroDivisionError:
                print("Currently holding zero shares.")
                pos['cost basis'] = 0
            pos['current shares'] = shares

    def shares_at_date(self, ticker, date):
        '''takes a ticker symbol, and a datetime.date() and returns the number
        of shares of that symbol held at the given date.'''
        shares = 0
        for pos in self.position_list:
            if pos['ticker'] == ticker:
                for transaction in pos['transactions']:
                    if int((date - parse_date(transaction['date'])).days) >= 0:
                        if transaction['b/s'] == 'b':
                            shares += transaction['shares']
                           
                        elif transaction['b/s'] == 's':
                            shares -= transaction['shares']
        return(shares)
                           
            

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
        year = today.year
        month = today.month
        day = today.day
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

    watch_list.enter_order(order[0].lower(),
                           date_str, tick,
                           shares,
                           price,
                           comm,
                           fee)
    watch_list.calc_cost_basis()

def view(pos):
    print("Ticker: {}".format(pos["ticker"]))
    print("Shares: {}".format(pos["current shares"]))
    print("Current cost basis: ${:<7.2f}".format(pos["cost basis"]))
    today = dt.date.today()
    try:
        df = web.DataReader(pos["ticker"],"yahoo",today)
        last_close = df["Close"][0]
        print("Current price: ${:<7.2f}\n".format(last_close))
    except:
        print("Current price data unavailable.")
        
    
    for t in pos["transactions"]:
        print("{}: {} {} @ ${:<7.4f}".format(t['date'],t['b/s'].upper(),
                                             t['shares'],t['price']))
    print("\n",end='')
    for d in pos['dividends']:
        print("Shares: {}; Dividend: ${:<7.2f}; Total: ${:<7.2f}"\
              .format(d['shares'],d['amount'],d['total']))

def edit(watch_list):
    print("\n",end='')
    edit_list = ['Transactions',
                 'Dividends',
                 'Tickers']
    viewlist = watch_list.list_positions() # used in several options
    edit_sel = edit_list[si.select(edit_list)]
    if edit_sel == 'Transactions':
        print("\n",end='')
        print("For which position would you like to edit a transaction?")
        
        edit_pos = viewlist[si.select(viewlist)]
        print("\nEditing",edit_pos,"\n")
        for pos in watch_list.position_list:
            if pos["ticker"] == edit_pos:
                print("Which transaction would you like to edit?")
                tran_list = []
                for t in pos["transactions"]:
                    trans_str = "{}: {} {} @ ${:<7.4f}".format(t['date'],t['b/s'].upper(),t['shares'],t['price'])
                    tran_list.append(trans_str)
                t_sel = tran_list[si.select(tran_list)]
                for i,t in enumerate(tran_list): # get index of transaction
                    if t_sel == t:
                        break
                    
                print("What would you like to edit?")
                edit_choices = ['Date',
                                'Buy/Sell',
                                'Shares',
                                'Price',
                                'Delete transaction']
                e_choice = edit_choices[si.select(edit_choices)]
                
                if e_choice == 'Date':
                    today = dt.date.today()
                    year = si.get_integer("Enter year.\n>>>",upper=today.year+1,lower=1970)
                    month = si.get_integer("Enter month.\n>>>",upper=13,lower=0)
                    day = si.get_integer("Enter day.\n>>>",upper=32,lower=0)
                    date_str = str(year)+'-'+str(month)+'-'+str(day)
                    
                    pos["transactions"][i]['date'] = date_str
                    
                elif e_choice == 'Buy/Sell':
                    orders = ['Buy',
                              'Sell']
                    print("What kind of order?")
                    order = orders[si.select(orders)]
                    
                    pos["transactions"][i]['b/s'] = order[0].lower()
                    
                elif e_choice == 'Shares':
                    shares = si.get_integer("Enter number of shares.\n>>>",lower=0)
                    
                    pos["transactions"][i]['shares'] = shares
                    
                elif e_choice == 'Price':
                    price = si.get_real_number("Enter share price.\n>>>",lower=0)

                    pos["transactions"][i]['price'] = price

                elif e_choice == 'Delete transaction':
                    pos["transactions"].pop(i)
                watch_list.calc_cost_basis()
                
    elif edit_sel == 'Dividends':
        pass
    elif edit_sel == 'Tickers':
        tick_options = ['Edit symbol',
                        'Delete symbol']
        
        print("Which ticker would you like to edit?")
        edit_pos = viewlist[si.select(viewlist)]
        print("What would you like to do with this position?")
        edit_sel = tick_options[si.select(tick_options)]
        for pos in watch_list.position_list:
            if pos["ticker"] == edit_pos:
                if edit_sel == 'Edit symbol':
                    tick = input("Enter stock ticker.\n>>>").upper()
                    pos["ticker"] = tick
                    # There will need to be logic here to merge two identical
                    # symbols.
                    
                elif edit_sel == 'Delete symbol':
                    pass
                                

def last_transaction_indicator(position):
    indicator = False
    score = 0
    # today's date
    today = dt.date.today()

    try:
        df = web.DataReader(position["ticker"],"yahoo",today)
        last_close = df["Close"][0]

        # Get last transaction
        last_t = position["transactions"][-1]

        # test for indicator
        if last_t['b/s'].lower() == 'b':
            if float(last_t['price']) < float(last_close):
                indicator = True
                score = (last_close - last_t['price']) * last_t['shares']
                direction = last_t['b/s']
            else:
                direction = 'N/A'

                
        elif last_t['b/s'].lower() == 's':
            if float(last_t['price']) > float(last_close):
                indicator = True
                score = (last_t['price'] - last_close) * last_t['shares']
                direction = last_t['b/s']
            else:
                direction = 'N/A'
    except:
        print("Indicator failed.")
                
    return(indicator, score, direction)

def parse_date(date):
    year,month,day = [int(x) for x in date.split('-')]
    d = dt.date(year,month,day)
    return(d)

def get_dividends(watch_list):
    '''This function gets a list of historical dividends for the given symbol,
    determines how many shares were held at each dividend date and adds a
    dividend transaction for each one to the position data. This function
    need only be run for dates after the most recent dividend transaction.'''
    for pos in watch_list.position_list:
        div_exists = False
        n = 0
        if len(pos['dividends']) == 0:
            print("No dividends have been recorded for {}.".format(pos['ticker']))
            # if no dividends have been recorded, find the earliest dated
            # transaction.
            date = parse_date(pos['transactions'][0]['date'])
        else:
            div_exists = True
            print("Latest recorded dividend was {}".format(pos['dividends'][-1]['date']))
            date = parse_date(pos['dividends'][-1]['date'])

        if pos['current shares'] > 0:
            div_df = web.DataReader(pos['ticker'],'yahoo-dividends',date)
            for stamp in div_df.index:
                year = stamp.year
                month = stamp.month
                day = stamp.day
                date_str = str(year)+'-'+str(month)+'-'+str(day)
                d = dt.date(year,month,day)
                delta = int((date - d).days)
                if delta > 0 or not div_exists:
                    n+=1
                    shares = watch_list.shares_at_date(pos['ticker'],d)
                    dividend = float(div_df.loc[stamp]['value'])
                    
                    watch_list.enter_dividend(pos['ticker'],
                                              date_str, dividend, shares)
        else:
            pass
            #print("Didn't fetch dividends. Not holding any shares.")
        print("processed {} dividends.".format(n))
        
        
                
    # Find the most recent dividend transaction posted in a position
    # Find the shares held at each dividend ex-date after the last one processed.
    # Add new dividend transactions

watch_list = positions()

style.use("fivethirtyeight")

print('\033[2J')
watch_list.load_positions()
watch_list.calc_cost_basis()
get_dividends(watch_list)
while(True):
    try:
        selections = ['Order',
                      'View',
                      'Indicators',
                      'Edit',
                      'Clear console',
                      'Save',
                      'Quit']
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
                
        elif selection == 'Indicators':
            ind_dict = {}
            
            for pos in watch_list.position_list:
                ind,score,direction = last_transaction_indicator(pos)
                #print comparison
                if ind:
                    
                    print("{} Score: ${:<7.2f} Last transaction: {}"\
                      .format(pos['ticker'],score,direction.upper()))
                else:
                    pass
            print("Done checking.\n")
                
        elif selection == 'Edit':
            edit(watch_list)
            
        elif selection == 'Clear console':
            print('\033[2J')
            # console command to clear console and return to (0,0)

        elif selection == 'Save':
            watch_list.save_positions()
            print("Saving...\n")
            
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
        #raise
    
##-example data structure-##
##positions = 
##[{'ticker':'TEST',
## 'transactions':[{'b/s':'buy','date':'2018-11-1','price':35.50,'commission':4.95,'fees':0.00,'shares':15},
##                 {'b/s':'sell','date':'2018-11-05','price':36.25,'commission':4.95,'fees':0.00,'shares':15},
##                 {'b/s':'buy','date':'2018-11-06','price':32.25,'commission':4.95,'fees':0.00,'shares':15}],
## 'dividends':[{'date':'2018-11-02','amount':0.15,'shares':15},
##              {'date':'2018-11-25','amount':0.12,'shares':15}],
## 'cost basis':32.22,
##  'current shares':15},
## {'ticker':'TEST2',
## 'transactions':[{'b/s':'buy','date':'2018-10-01','price':12.40,'commission':4.95,'fees':0.00,'shares':100},
##                 {'b/s':'sell','date':'2018-10-05','price':13.10,'commission':4.95,'fees':0.00,'shares':70},
##                 {'b/s':'buy','date':'2018-11-06','price':9.15,'commission':4.95,'fees':0.00,'shares':200}],
## 'dividends':[{'date':'2018-10-02','amount':0.07,'shares':100},
##              {'date':'2018-11-25','amount':0.11,'shares':230}],
## 'cost basis':9.285,
##  'current shares':230}]
