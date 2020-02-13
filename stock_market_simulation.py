import numpy as np
import yfinance as yf
import pandas as pd
from random import randint
import matplotlib.pyplot as plt

class Trader:
    
    def __init__(self, stock_prices, buy_or_sell):
        if len(stock_prices) != len(buy_or_sell):
            raise AttributeError("buy_or_sell actions list size has to be equal to stock_prices list size!")
        self.stock_prices = stock_prices
        self.buy_or_sell = buy_or_sell
        self.capital = 10000 # USD
        self.buying_rate = 1 # per day
        self.amount_of_stock = 10
        self.history = []
        self.timing = 'Open' # When buying and selling will take place
        print(self.buy_or_sell)
    
    def stock_action(self):
        print(self.buy_or_sell)

        for counter, action in enumerate(self.buy_or_sell):
            if action >= 1:
                self.buy_if_money(action,counter)
            if action < 0:
                self.sell_if_stock(abs(action),counter)
            self.print_state(counter)
        self.visualize_money()

    def buy_if_money(self, amount, day):
        stock_price = self.stock_prices.iloc[day][self.timing]
        amount_to_buy = min(amount,int(self.capital/stock_price)) # if we can't buy as many as we like, 
        #we buy the most we can
        self.capital = self.capital - amount_to_buy*stock_price
        self.amount_of_stock = self.amount_of_stock + amount_to_buy
        if amount > int(self.capital/stock_price):
            print("couldn't buy all we wanted")


    def sell_if_stock(self,amount,day):
        stock_price = self.stock_prices.iloc[day][self.timing]
        amount_to_sell = min(amount,self.amount_of_stock) # if we can't sell as many as we like, 
        #we sell the most we can
        self.capital = self.capital + amount_to_sell*stock_price
        self.amount_of_stock = self.amount_of_stock - amount_to_sell
        if amount > self.amount_of_stock:
            print("couldn't sell all we wanted")

    def print_state(self,counter):
        stock_price = self.stock_prices.iloc[counter][self.timing]
        self.history.append(self.capital + self.amount_of_stock * stock_price)
        print(f"Day {counter}, Amount of Stock: {self.amount_of_stock}, Capital: {self.capital}, Net Worth= {self.capital+self.amount_of_stock*stock_price}")
    
    def visualize_money(self):
        plt.plot(np.arange(1, len(self.history) + 1), self.history)
        plt.ylabel('Net Worth in $')
        plt.xlabel('trading day')
        plt.ylim((12000,14000))
        plt.hlines(self.history[0],0,len(self.history),linestyles="dashed",label="starting amount")
        plt.show()

def load_stock_prices_from_json(path="./processed_data/stock/stocks_cleaned.json"):
    return pd.read_json(path)

def load_stock_prices_from_yahoo_finance(start='2018-01-01', end='2018-06-05'):
    tesla = yf.Ticker("TSLA")
    return tesla.history(start=start, end=end)

def get_random_actions(size=100):
    return [randint(-2,2) for x in range(random_list)]