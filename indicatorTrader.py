import time
import Exchange.Binance
import Exchange.Kucoin
import ccxt
import queue
import math

counter = 0


class indicatorTrader():

    def __init__(self):
        self.exchanges = [
            Exchange.Binance.binance()
        ]
        self.coins = [
            'LTC',
            'ARK',
            'GTO',
            'APPC',
            'NANO',
            'ZRX',
            'BCC',
            'ETC',
            'NEBL',
            'PPT',
            'HSR',
            'INS',
            'EOS',
            'OMG',
            'POE',
            'WTC',
            'BRD',
            'XMR',
            'IOTA',
            'TRIG',
            'ADX',
            'GVT',
            'QTUM',
            'WABI',
            'BLZ',
            'WAVES',
            'SALT',
            'AION',
            'GAS',
            'ZEC',
            'BCD',
            'DGD',
            'ARN',
            'SUB',
            'ENG',
            'KMD',
            'FUN',
            'VIB',
            'BQX',
            'REQ',
            'QSP',
            'OST',
            'MANA',
            'LUN',
            'XZC',
            'NULS',
            'PIVX',
            'POWR', ]
        self.maxBuy = 0.002
        self.orders = {}
        self.emas = {}
        self.rsi= {}
        self.nextTrade = {}
        for coin in self.coins:
            self.emas[coin] = {'12': 0, '26': 0, '9': 0,'momentumSignal': 0,'signal': 0, }
            # Momentum, 0 = away from 0; 1 = closer to 0
            # Signal, 0 = do nothing, 1 = buy, 2 = sell
            self.rsi[coin] = {'price': 0,'past14': [0 for i in range(14)],'rsi': 0,'signal': 0}
            # Signal, 0 = do nothing, 1 = buy, 2 = sell
            self.nextTrade[coin] = 0
    def setAPI(self):
        self.exchanges[0].apiKey = ''
        self.exchanges[0].secret = ''
        self.exchanges[0].updateMarkets()
    def loadIndicatorData(self):
        for coin in self.coins:
            prices = self.exchanges[0].fetch_ohlcv(coin + "/BTC",'5m')
            for price in prices:
                self.updateIndicators(coin,price[4])
    def loadOrders(self):
        self.resetOrders()
        for exchange in self.exchanges:
            self.orders = exchange.loadAllOpenOrders(self.orders)
    def updateIndicators(self,coin,newPrice):
        self.upDateEmas(coin,newPrice)
        self.upDateRSI(coin,newPrice)
    def upDateRSI(self,coin,newPrice):
        change = newPrice - self.rsi[coin]['price']
        self.rsi[coin]['price'] = newPrice
        self.rsi[coin]['past14'].append(change)
        self.rsi[coin]['past14'] = self.rsi[coin]['past14'][1:]
        avgGain = 0
        avgLoss = 0
        for i in self.rsi[coin]['past14']:
            if i > 0:
                avgGain+= i
            else:
                avgLoss -= i
        avgGain /= 14
        avgLoss /= 14
        if avgLoss == 0:
            newRsi = 100
            self.rsi[coin]['rsi'] = newRsi
        else:
            newRsi = 100 - (100/(1+(avgGain/avgLoss)))
            self.rsi[coin]['rsi'] = newRsi
        if newRsi >= 70:
            self.rsi[coin]['signal'] = 2
        elif newRsi <= 25:
            self.rsi[coin]['signal'] = 1
        elif 65 >= newRsi >= 30:
            self.rsi[coin]['signal'] = 0

        # print("Change: " + str(change) + "\nRSI: " + str(self.rsi[coin]['rsi']))
        # print("Signal: " + str(self.rsi[coin]['signal']))
    def upDateEmas(self,coin,newPrice):
        lastEma12 = self.emas[coin]['12']
        if lastEma12 == 0: ema12 = (newPrice - lastEma12) + lastEma12
        else: ema12 = (newPrice - lastEma12) * 2/13 + lastEma12
        self.emas[coin]['12'] = ema12
        lastEma26 = self.emas[coin]['26']
        if lastEma26 == 0: ema26 = (newPrice - lastEma26) + lastEma26
        else: ema26 = (newPrice - lastEma26) * 2/27 + lastEma26
        self.emas[coin]['26'] = ema26
        macd = ema12 - ema26
        lastEma9 = self.emas[coin]['9']
        if lastEma9 == 0: ema9 = (macd - lastEma9) + lastEma9
        else: ema9 = (macd - lastEma9) * 2/10 + lastEma9
        self.emas[coin]['9'] = ema9
        if (abs((lastEma12-lastEma26-lastEma9)) - abs((macd-ema9))) > 0:
            self.emas[coin]['momentumSignal'] = 1
            if macd > 0 and ema9 > 0 and (macd-ema9) > 0:
                self.emas[coin]['signal'] = 2
            elif macd < 0 and ema9 < 0 and (macd-ema9) < 0:
                self.emas[coin]['signal'] = 1
            else:
                self.emas[coin]['signal'] = 0
        else:
            self.emas[coin]['momentumSignal'] = 0
            self.emas[coin]['signal'] = 0

        # print("Price: " + str(newPrice) + "\nMACD: " + str(macd) + "\nEMA9: " + str(ema9))
        # print("Histogram: " + format((macd-ema9),'.15f'))
        # print("Iteration: " + str(counter))
        # print("Momentum: " + str(self.emas[coin]['momentumSignal']))
        # print("Signal: " + str(self.emas[coin]['signal']))
    def upDateTradeTimes(self):
        for coin in self.nextTrade:
            if self.nextTrade[coin] > 0:
                self.nextTrade[coin] -= 1

    def manageTrades(self):
        base="BTC"
        for coin in self.coins:
            for exchange in self.exchanges:
                if exchange.isSybmolInMarket(coin,base):
                    try:
                        openOrders = exchange.fetch_open_orders(coin + "/" + base)
                        orderBook = exchange.fetch_order_book(coin + '/' + base)
                        self.updateIndicators(coin,((orderBook['bids'][0][0]+orderBook['asks'][0][0])/2))
                    except:
                        openOrders = 'Failed'
                    if openOrders == "Failed":
                        print("Couldn't fetch orders for: " + str(coin))
                        continue
                    elif len(openOrders) == 1:
                        side = openOrders[0]['side']
                        if self.nextTrade[coin] == 0:
                            if side == "buy":
                                self.makeOrder("SELL", coin, base, exchange)
                            elif side == "sell":
                                self.makeOrder("BUY", coin, base, exchange)
                    elif len(openOrders) == 2:
                        side = 'both'
                    elif len(openOrders) == 0:
                        side = 'none'
                        if self.nextTrade[coin] == 0:
                            self.makeOrder("BUY",coin,base,exchange)
                            self.makeOrder("SELL", coin, base, exchange)
                    else:
                        print(openOrders)
                        raise(WindowsError)
                    if side != 'none':
                        self.upDateTrades(side,coin,base,exchange)
    def upDateTrades(self,side,coin,base,exchange):
        try:
            orderBook = exchange.fetch_order_book(coin + '/' + base)
        except:
            return
        if side == 'buy' or side == "both":
            if orderBook['bids'][2][0] > self.orders[coin]['BUY']['price']:
                try:
                    exchange.cancel_order(self.orders[coin]["BUY"]['id'],coin + '/' + base)
                    print("Canceled buy order for: " + coin)
                    self.makeOrder("BUY",coin,base,exchange)
                except ccxt.RequestTimeout:
                    print("Error in upDateTrades: Timeout")
                    time.sleep(60)
        if side == 'sell' or side == "both":
            if orderBook['asks'][2][0] < self.orders[coin]['SELL']['price']:
                try:
                    exchange.cancel_order(self.orders[coin]["SELL"]['id'],coin + '/' + base)
                    print("Canceled sell order for: " + coin)
                    self.makeOrder("SELL",coin,base,exchange)
                except ccxt.RequestTimeout:
                    print("Error in upDateTrades: Timeout")
                    time.sleep(60)

    def makeOrder(self,side,coin,base,exchange):
        try:
            orderBook = exchange.fetch_order_book(coin + '/' + base)
        except:
            return
        lowAsk1 = orderBook['asks'][0][0]
        highBid1 = orderBook['bids'][0][0]
        if self.emas[coin]['signal'] == 2 and self.rsi[coin]['signal'] == 2 and side == "SELL":
            coinBalance = exchange.fetch_free_balance()[coin]
            if coinBalance*highBid1 < 0.001:
                return
            sellPrice = lowAsk1*0.9995
            if coinBalance*highBid1 > self.maxBuy*2.2*2:
                sellAmount = (self.maxBuy*2.2*2/sellPrice)
            else:
                sellAmount = coinBalance
            orderReturn = exchange.create_limit_sell_order(coin + "/" + base,sellAmount,sellPrice)
            self.orders[coin][side] = {'id': orderReturn['id'], 'price': orderReturn['price'], 'amount':orderReturn['amount']}
            self.nextTrade[coin] = 3  # Not allowed new trade within 3 time units
            print('Made sell order for ' + coin + " @" + str(sellPrice))
            print("RSI: " + str(self.rsi[coin]['rsi']))
            print("Macd: " + str(self.emas[coin]['12'] - self.emas[coin]['26']))
            print("EMA9: " + str(self.emas[coin]['9']))
        elif self.emas[coin]['signal'] == 1 and self.rsi[coin]['signal'] == 1 and side == "BUY":
            coinBalance = exchange.fetch_free_balance()[coin]
            if exchange.fetch_free_balance()["BTC"] < self.maxBuy*1.01:
                print("BTC balance too low for coin " + coin)
                return
            if coinBalance*highBid1 > 0.03:
                print("Too much of coin " + coin)
                return
            buyPrice = highBid1*1.0005
            orderReturn = exchange.create_limit_buy_order(coin + "/" + base,(self.maxBuy/buyPrice),buyPrice)
            self.orders[coin][side] = {'id': orderReturn['id'], 'price': orderReturn['price'], 'amount':orderReturn['amount']}
            self.nextTrade[coin] = 3  # Not allowed new trade within 3 time units
            print('Made buy order for ' + coin + " @" + str(buyPrice))
            print("RSI: " + str(self.rsi[coin]['rsi']))
            print("Macd: " + str(self.emas[coin]['12'] - self.emas[coin]['26']))
            print("EMA9: " + str(self.emas[coin]['9']))



    def resetOrders(self):
        for coin in self.coins:
            self.orders[coin] = {"BUY": {},"SELL":{}}





trader = indicatorTrader()
trader.setAPI()
trader.loadIndicatorData()
trader.loadOrders()
while True:
    start = time.time()
    trader.manageTrades()
    trader.upDateTradeTimes()
    counter += 1
    timeTaken = time.time() - start
    if 300-timeTaken > 0:
        time.sleep(300-timeTaken)