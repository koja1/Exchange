import math
import time
import re
from bs4 import BeautifulSoup
import requests
import json
import Binance
import Kucoin


class marginTrader():

    def __init__(self):
        self.exchanges = [
            Binance.binance()
        ]
        self.coins = ['NEO','LTC''ARK']
        self.maxBuy = 0.01
        self.orders = {}

    def setAPI(self):
        self.exchanges[0].apiKey = 'Lx1DB2sU8sOO19tx56V248pBn2pLelM6bMNBRiLbTPA1xdYVpHxaqn4DkQGYoU0M'
        self.exchanges[0].secret = 'tzioDoQ4hFAUvUJpfvU9SB8bwjQlsjE50k579lzIWQgGYvod1TC2YmtqeW5YyZEm'
        self.exchanges[0].updateMarkets()
    def manageTrades(self):
        base="BTC"
        for coin in self.coins:
            for exchange in self.exchanges:
                if exchange.isSybmolInMarket(coin,base):
                    openOrders = exchange.fetch_open_orders(coin + "/" + base)
                    side = ''
                    if len(openOrders) == 1:
                        side = openOrders[0]['side']
                    elif len(openOrders) == 2:
                        side = 'both'
                    elif len(openOrders) == 0:
                        side = 'none'
                        self.makeOrder("BUY",coin,base,exchange)
                    else: raise(WindowsError)

    def makeOrder(self,side,coin,base,exchange):
        lowAsk1 = exchange.fetch_order_book(coin + '/' + base)['asks'][0]
        lowAsk2 = exchange.fetch_order_book(coin + '/' + base)['asks'][1]
        highBid1 = exchange.fetch_order_book(coin + '/' + base)['bids'][0]
        highBid2 = exchange.fetch_order_book(coin + '/' + base)['bids'][1]
        if lowAsk1[0]/highBid1[0] < 1.005:
            return
        numberDecimals = max(len(str(lowAsk1[0])),len(str(lowAsk2[0])),len(str(highBid1[0])), len(str(highBid2[0]))) - 2
        self.orders[coin] = {"BUY": {},"SELL":{}}
        if side == "BUY":
            if lowAsk2[0]/lowAsk1[0] < 1.002 and lowAsk1[1]*lowAsk1[0] > 0.005:
                buyPrice = (lowAsk1[0]*math.pow(10,numberDecimals)+1)/math.pow(10,numberDecimals)
            else:
                buyPrice = (lowAsk2[0] * math.pow(10, numberDecimals) + 1) / math.pow(10, numberDecimals)
            orderReturn = exchange.create_limit_buy_order(coin + "/" + base,(self.maxBuy/buyPrice),buyPrice)
            self.orders[coin][side] = {'id': orderReturn['id'], 'price': orderReturn['price'], 'amount':orderReturn['amount']}
            print('Made order for ' + coin + " @" + str(buyPrice))
            print(orderReturn)
        elif side == "SELL":
            if highBid2[0]/highBid1[0] > 1.002 and highBid1[1]*highBid1[0] > 0.005:
                sellPrice = (highBid1[0]*math.pow(10,numberDecimals)-1)/math.pow(10,numberDecimals)
            else:
                sellPrice = (highBid2[0] * math.pow(10, numberDecimals) - 1) / math.pow(10, numberDecimals)
            orderReturn = exchange.create_limit_sell_order(coin + "/" + base,exchange.fetch_free_balance()[coin],sellPrice)
            self.orders[coin][side] = {'id': orderReturn['id'], 'price': orderReturn['price'], 'amount':orderReturn['amount']}





trader = marginTrader()
trader.setAPI()
while True:
    trader.manageTrades()
    time.sleep(10)
    print('\n')