import datetime as dt
import time
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import json
import sys
import os
import sanitize_inputs as si

__version__ = '0.6.1'
#os.system("mode con cols=60 lines=60")

# Hide all warnings
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
    
class positions():
    def __init__(self):
        self.position_list = []

    def list_positions(self):
        plist = []
        for pos in self.position_list:
            plist.append(pos['ticker'])
        return(plist)
    
    def enter_order(self, buysell, date, ticker, shares, price,
                    commission=4.95, fees=0):
        '''buysell = 'buy' or 'sell', date of order(str), stock ticker (not case
        sensitive), price of order, number of shares transacted,
        commission, and fees if applicable.'''
        exists_flag = False
        ticker = ticker.upper()
        for pos in self.position_list:
            if ticker == pos['ticker']:
                exists_flag = True
                print("Position is already on watch list")
                pos['transactions'].append({'b/s':buysell,
                                            'date':date,
                                            'price':price,
                                            'commission':commission,
                                            'fees':fees,'shares':shares})
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
                print("Shares: {}; Dividend: ${:<7.2f}; Total: ${:<7.2f}"\
                      .format(shares,amount,total))
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
        year = si.get_integer("Enter year.\n>>>",
                              upper=today.year+1,lower=1970)
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

    df = get_quoteDF(pos["ticker"],"yahoo",today)

    last_close = df["Close"][0]
    print("Current price: ${:<7.2f}\n".format(last_close))
        
    print("Transactions:")
    for t in pos["transactions"]:
        print("{}: {} {} @ ${:<7.4f}".format(t['date'],t['b/s'].upper(),
                                             t['shares'],t['price']))
    print("\nDividends:")
    for d in pos['dividends']:
        print("{}: {} x ${:<7.2f} = ${:<7.2f}"\
              .format(d['date'],d['shares'],d['amount'],d['total']))

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
                    trans_str = "{}: {} {} @ ${:<7.4f}"\
                                .format(t['date'],
                                        t['b/s'].upper(),
                                        t['shares'],
                                        t['price'])
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
                    year = si.get_integer("Enter year.\n>>>",
                                          upper=today.year+1,lower=1970)
                    month = si.get_integer("Enter month.\n>>>",
                                           upper=13,lower=0)
                    day = si.get_integer("Enter day.\n>>>",
                                         upper=32,lower=0)
                    date_str = str(year)+'-'+str(month)+'-'+str(day)
                    
                    pos["transactions"][i]['date'] = date_str
                    
                elif e_choice == 'Buy/Sell':
                    orders = ['Buy',
                              'Sell']
                    print("What kind of order?")
                    order = orders[si.select(orders)]
                    
                    pos["transactions"][i]['b/s'] = order[0].lower()
                    
                elif e_choice == 'Shares':
                    shares = si.get_integer("Enter number of shares.\n>>>",
                                            lower=0)
                    
                    pos["transactions"][i]['shares'] = shares
                    
                elif e_choice == 'Price':
                    price = si.get_real_number("Enter share price.\n>>>",
                                               lower=0)

                    pos["transactions"][i]['price'] = price

                elif e_choice == 'Delete transaction':
                    pos["transactions"].pop(i)
                watch_list.calc_cost_basis()
                
    elif edit_sel == 'Dividends':
        print("For which position would you like to edit a dividend?")
        edit_pos = viewlist[si.select(viewlist)]
        for pos in watch_list.position_list:
            if pos["ticker"] == edit_pos:
                print("Which dividend would you like to edit?")
                div_list = []
                for d in pos["dividends"]:
                    div_str = "{}: {} x ${:<7.2f} = ${:<7.2f}"\
                                .format(d['date'],
                                        d['shares'],
                                        d['amount'],
                                        d['total'])
                    
                    div_list.append(div_str)
                d_sel = div_list[si.select(div_list)]
                for i,d in enumerate(div_list): # get index of transaction
                    if d_sel == d:
                        break
                    
                print("What would you like to edit?")
                edit_choices = ['Date',
                                'Amount',
                                'Shares',
                                'Total',
                                'Delete dividend']
                
                e_choice = edit_choices[si.select(edit_choices)]
                if e_choice == 'Date':
                    today = dt.date.today()
                    year = si.get_integer("Enter year.\n>>>",
                                          upper=today.year+1,lower=1970)
                    month = si.get_integer("Enter month.\n>>>",
                                           upper=13,lower=0)
                    day = si.get_integer("Enter day.\n>>>",
                                         upper=32,lower=0)
                    date_str = str(year)+'-'+str(month)+'-'+str(day)
                    
                    pos["dividends"][i]['date'] = date_str
                    
                elif e_choice == 'Amount':
                    amount = si.get_real_number("Enter dividend amount.\n>>>",
                                               lower=0)
                    pos["dividends"][i]['amount'] = amount
                elif e_choice == 'Shares':
                    shares = si.get_integer("Enter number of shares.\n>>>",
                                            lower=0)
                    
                    pos["dividends"][i]['shares'] = shares
                    
                elif e_choice == 'Total':
                    price = si.get_real_number("Enter total dividend.\n>>>",
                                               lower=0)
                    pos["dividends"][i]['total'] = price

                elif e_choice == 'Delete dividend':
                    pos["dividends"].pop(i)
                watch_list.calc_cost_basis()
                    
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
                                
def last_transaction_indicator(watch_list, ind_dict):
    indicator = False
    score = 0
    # today's date
    today = dt.date.today()

    for index, position in enumerate(watch_list.position_list):
        # The next few lines print progress indication
        print("\033[1A\033[K", end='')
        # \033[K = Erase to the end of line
        # \033[1A = moves the cursor up 1 line.
        print("{}/{}".format(index,len(watch_list.position_list),end=''))
        
        indicator = False
        score = 0
        try:
            df = web.DataReader(position["ticker"],"yahoo",today)
            last_close = df["Close"][0]

            position["last price"] = last_close
            year,month,day = unpack_date(today)

            position["last price date"] = \
                           str(year)+'-'+str(month)+'-'+str(day)
            # Get last transaction
            last_t = position["transactions"][-1]

            # test for indicator
            if last_t['b/s'].lower() == 'b':
                # Note that this logic assumes a $4.95 commission and $0 fee.
                if (float(last_t['price'])
                    +(4.95/last_t['shares']) < float(last_close)):
                    
                    indicator = True
                    score = (last_close - last_t['price']) * last_t['shares']
                    direction = last_t['b/s']
                else:
                    direction = 'N/A'
   
            elif last_t['b/s'].lower() == 's':
                # Note that this logic assumes a $4.95 commission and $0 fee.
                if (float(last_t['price']) > float(last_close)
                    +(4.95/last_t['shares'])):
                    
                    indicator = True
                    score = (last_t['price'] - last_close) * last_t['shares']
                    direction = last_t['b/s']
                else:
                    direction = 'N/A'
            if direction.lower() == 'b':
                direction = 'SELL'
            elif direction.lower() == 's':
                direction = 'BUY'
            else:
                pass
                
        except:
            print("Indicator failed.")
        if indicator:
            ind_dict["Last Transaction"].append \
                           ({"Ticker":position['ticker'],
                             "Score":score,
                             "Direction":direction.upper()})
        else:
            pass
  
    return(watch_list, ind_dict)

def div_yield_indicator(watch_list, ind_dict):
    indicator = False
    score = 0
    direction = 'b'
    # today's date
    today = dt.date.today()
    last_year = dt.date(today.year-1,1,1)

    for index,position in enumerate(watch_list.position_list):
        # The next few lines print progress indication
        print("\033[1A\033[K", end='')
        # \033[K = Erase to the end of line
        # \033[1A = moves the cursor up 1 line.
        print("{}/{}".format(index,len(watch_list.position_list),end=''))
        
        try:
            df = web.DataReader(position["ticker"],"yahoo",today)
            last_close = df["Close"][0]

            div_df = web.DataReader(position['ticker'],
                                    'yahoo-dividends',last_year)
            dividend = div_df['value'][0]

            score = (dividend/last_close)*4 # assumes quarterly dividend.
            direction = "N/A"
            ind_dict["High Dividend Yield"].append \
                           ({"Ticker":position['ticker'],
                             "Score":score,
                             "Direction":direction.upper()})
        except:
            pass
        
    return(watch_list, ind_dict)

def parse_date(date):
    year,month,day = [int(x) for x in date.split('-')]
    d = dt.date(year,month,day)
    return(d)

def unpack_date(date):
    year=date.year
    month=date.month
    day=date.day
    return(year,month,day)

def get_dividends(watch_list, force_all=False):
    '''This function gets a list of historical dividends for the given symbol,
    determines how many shares were held at each dividend date and adds a
    dividend transaction for each one to the position data. This function
    need only be run for dates after the most recent dividend transaction.
    force_all will find dividends for positions for which no shares are
    currently held.'''
    for pos in watch_list.position_list:
        div_exists = False
        n = 0
        if len(pos['dividends']) == 0:
            print("No dividends have been recorded for {}."\
                  .format(pos['ticker']))
            # if no dividends have been recorded, find the earliest dated
            # transaction.
            date = parse_date(pos['transactions'][0]['date'])
        else:
            div_exists = True
            print("{}: Latest recorded dividend was {}"\
                  .format(pos["ticker"],pos['dividends'][0]['date']))
            date = parse_date(pos['dividends'][0]['date'])
            
        #date = parse_date(pos['transactions'][0]['date'])
        if pos['current shares'] > 0 or force_all:
            div_df = web.DataReader(pos['ticker'],'yahoo-dividends',date)
            for stamp in div_df.index:
                year,month,day = unpack_date(stamp)

                date_str = str(year)+'-'+str(month)+'-'+str(day)
                d = dt.date(year,month,day)
                delta = int((date - d).days)
                if delta < 0 or not div_exists:
                    print("processing dividend.")
                    n+=1
                    shares = watch_list.shares_at_date(pos['ticker'],d)
                    dividend = float(div_df.loc[stamp]['value'])
                    
                    watch_list.enter_dividend(pos['ticker'],
                                              date_str, dividend, shares)
                else:
                    print("{}: dividends are up to date.".format(pos['ticker']))
        else:
            pass
            #print("Didn't fetch dividends. Not holding any shares.")
        print("processed {} dividends.".format(n))

def timeout_handler(num, stack):
    raise Exception("Timeout")

def get_divDF(ticker,source,date):
    try:
        div_df = web.DataReader(ticker,source,date)
    except Exception as ex:
        print(ex)
        print("No response from yahoo-finance.")

    finally:
        signal.alarm(0)
        
    return(div_df)

def get_quoteDF(ticker,source,date):
    try:
        df = web.DataReader(ticker,source,date)
    except Exception as ex:
        print(ex)
        print("No response from yahoo-finance.")
    
    return(df)

watch_list = positions()

style.use("fivethirtyeight")

print('\033[2J') # Clear the terminal
watch_list.load_positions()
watch_list.calc_cost_basis()

while(True):
    try:
        selections = ['Order',
                      'View',
                      'Indicators',
                      'Edit',
                      'Other',
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
            ind_dict = {"Last Transaction":[],
                        "High Dividend Yield":[],
                        "Recent Passed Dividend":[],
                        "Upcoming Dividend":[],
                        "Over-exposure":[]}
            
            print("\nWorking on \"Last Transaction\" indicator.\n")
            watch_list, ind_dict = last_transaction_indicator(watch_list,
                                                              ind_dict)
            print("\033[1A\033[K", end='')    
            print("Done checking.\n")

            for indicator in ind_dict["Last Transaction"]:
                print("{:<6} Score: ${:<7.2f} Advise: {}".format\
                      (indicator["Ticker"],
                       indicator["Score"],
                       indicator["Direction"].upper()))
            print("\n",end='')
            
            print("\nWorking on \"Dividend Yield\" indicator.\n")
            watch_list, ind_dict = div_yield_indicator(watch_list,ind_dict)

            for indicator in ind_dict["High Dividend Yield"]:
                print("{:<6} Score: {:<7.2f}% Advise: {}".format\
                      (indicator["Ticker"],
                       indicator["Score"]*100,
                       indicator["Direction"].upper()))
            print("\n",end='')
            
            for indicator in ind_dict["Recent Passed Dividend"]:
                pass
        elif selection == 'Edit':
            edit(watch_list)

        elif selection == 'Other':
            print('\n',end='')
            selections = ['Get all dividends',
                          'Get dividends for current positions',
                          'Clear console']
            selection = selections[si.select(selections)]
            if selection == 'Get all dividends':
                get_dividends(watch_list, force_all=True)

            elif selection == 'Get dividends for current positions':
                get_dividends(watch_list)
                
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
        time.sleep(60)
        #continue
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
##  'current shares':230,
##  'last price': 5.43,
##  'last price date':'2018-12-20'}]
