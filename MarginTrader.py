import math
import time
import re
from bs4 import BeautifulSoup
import requests
import json
import Exchange.Binance
import Exchange.Kucoin


counter = 0


class marginTrader():

    def __init__(self):
        self.exchanges = [
            Exchange.Binance.binance()
        ]
        self.coins = [
            'NEO',
            'LTC',
            'ARK',
            'TRX',
            'ETH',
            'GTO',
            'VEN',
            'APPC',
            'NANO',
            'XRP',
            'ZRX',
            'ICX',
            'BCC',
            'ETC',
            'ADA',
            'VIBE',
            'XVG',
            'NEBL',
            'PPT',
            'HSR',
            'INS',
            'EOS',
            'OMG',
            'XLM',
            'POE',
            'RPX',
            'LSK',
            'WTC',
            'BRD',
            'XMR',
            'LINK',
            'IOTA',
            'TRIG',
            'ADX',
            'GVT',
            'CND',
            'QTUM',
            'GXS',
            'WABI',
            'AMB',
            'BLZ',
            'WAVES',
            'SALT',
            'CHAT',
            'KNC',
            'AION',
            'GAS',
            'ELF',
            'ZEC',
            'ENJ',
            'BCD',
            'DASH',
            'BCPT',
            'BTG',
            'DGD',
            'BTS',
            'STRAT',
            'ARN',
            'SUB',
            'ENG',
            'KMD',
            'FUN',
            'VIB',
            'BQX',
            'REQ',
            'FUEL',
            'QSP',
            'OST',
            'MANA',
            'LUN',
            'STORJ',
            'XZC',
            'NULS',
            'PIVX',
            'DLT',
            'SNT',
            'POWR']
        self.maxBuy = 0.015
        self.orders = {}

    def setAPI(self):
        self.exchanges[0].apiKey = 'Lx1DB2sU8sOO19tx56V248pBn2pLelM6bMNBRiLbTPA1xdYVpHxaqn4DkQGYoU0M'
        self.exchanges[0].secret = 'tzioDoQ4hFAUvUJpfvU9SB8bwjQlsjE50k579lzIWQgGYvod1TC2YmtqeW5YyZEm'
        self.exchanges[0].updateMarkets()

    def loadOrders(self):
        self.resetOrders()
        for exchange in self.exchanges:
            self.orders = exchange.loadAllOpenOrders(self.orders)
    def manageTrades(self):
        base="BTC"
        for coin in self.coins:
            for exchange in self.exchanges:
                if exchange.isSybmolInMarket(coin,base):
                    try:
                        openOrders = exchange.fetch_open_orders(coin + "/" + base)
                    except:
                        openOrders = 'Failed'
                    if openOrders == "Failed":
                        print("Couldn't fetch orders for: " + str(coin))
                        continue
                    elif len(openOrders) == 1:
                        side = openOrders[0]['side']
                    elif len(openOrders) == 2:
                        side = 'both'
                    elif len(openOrders) == 0:
                        side = 'none'
                        self.makeOrder("BUY",coin,base,exchange)
                    else:
                        print(openOrders)
                        raise(WindowsError)
                    if side != 'none' and counter % 3 == 0:
                        self.upDateTrades(side,coin,base,exchange)
                    if side == "buy" or side == "none":
                        try:
                            self.makeOrder("SELL",coin,base,exchange)
                        except:
                            pass
    def upDateTrades(self,side,coin,base,exchange):
        try:
            orderBook = exchange.fetch_order_book(coin + '/' + base)
        except:
            return
        if side == 'buy' or side == "both":
            if orderBook['bids'][2][0] > self.orders[coin]['BUY']['price']:
                exchange.cancel_order(self.orders[coin]["BUY"]['id'],coin + '/' + base)
                print("Canceled buy order for: " + coin)
                self.makeOrder("BUY",coin,base,exchange)
        elif side == 'sell' or side == "both":
            if orderBook['asks'][2][0] < self.orders[coin]['SELL']['price']:
                exchange.cancel_order(self.orders[coin]["SELL"]['id'],coin + '/' + base)
                print("Canceled sell order for: " + coin)
                self.makeOrder("SELL",coin,base,exchange)

    def makeOrder(self,side,coin,base,exchange):
        try:
            orderBook = exchange.fetch_order_book(coin + '/' + base)
        except:
            return
        lowAsk1 = orderBook['asks'][0]
        lowAsk2 = orderBook['asks'][1]
        highBid1 = orderBook['bids'][0]
        highBid2 = orderBook['bids'][1]
        if lowAsk1[0]/highBid1[0] < 1.002:
            print(coin)
            print("Bid: " + str(highBid1[0]) + "\nAsk: " + str(lowAsk1[0]) + "\nMargin: " + str(lowAsk1[0]/highBid1[0]))
            return
        if side == "SELL" and exchange.fetch_free_balance()[coin]*exchange.getSymbolMarket(coin,"BTC")['bid'] > 0.002:
            if lowAsk2[0] / lowAsk1[0] < 1.002 and lowAsk1[1] * lowAsk1[0] > 0.01:
                sellPrice = lowAsk1[0]*0.9999
            else:
                sellPrice = lowAsk2[0]*0.9999
            orderReturn = exchange.create_limit_sell_order(coin + "/" + base,exchange.fetch_free_balance()[coin],sellPrice)
            self.orders[coin][side] = {'id': orderReturn['id'], 'price': orderReturn['price'], 'amount':orderReturn['amount']}
            print('Made sell order for ' + coin + " @" + str(sellPrice))
            return
        if lowAsk1[0]/highBid1[0] < 1.0045:
            print(coin)
            print("Bid: " + str(highBid1[0]) + "\nAsk: " + str(lowAsk1[0]) + "\nMargin: " + str(lowAsk1[0]/highBid1[0]))
            return
        if side == "BUY":
            if exchange.fetch_free_balance()["BTC"] < self.maxBuy*1.01:
                print("BTC balance too low")
                return
            if highBid2[0] / highBid1[0] > 1.002 and highBid1[1] * highBid1[0] > 0.01:
                buyPrice = highBid1[0]*1.0001
            else:
                buyPrice = highBid2[0]*1.0001
            orderReturn = exchange.create_limit_buy_order(coin + "/" + base,(self.maxBuy/buyPrice),buyPrice)
            self.orders[coin][side] = {'id': orderReturn['id'], 'price': orderReturn['price'], 'amount':orderReturn['amount']}
            print('Made buy order for ' + coin + " @" + str(buyPrice))


    def resetOrders(self):
        for coin in self.coins:
            self.orders[coin] = {"BUY": {},"SELL":{}}





trader = marginTrader()
trader.setAPI()
trader.loadOrders()
while True:
    trader.manageTrades()
    counter += 1
    time.sleep(60)
    print('\n')