import math
import time
import re
from bs4 import BeautifulSoup
import requests
import json
import ccxt
import Exchange.Binance
import Exchange.Kucoin
import Exchange.Cryptopia


class arbitrage():

    def __init__(self):
        self.exchanges = [
            Exchange.Binance.binance(),
            Exchange.Kucoin.kucoin(),
            Exchange.Cryptopia.cryptopia()
        ]
        self.coins = [
            'BTC',
            'ETH',
            'XRP',
            'BCH',
            'ADA',
            'LTC',
            'XLM',
            'NEO',
            'EOS',
            'XEM',
            'MIOTA',
            'DASH',
            'XMR',
            'LSK',
            'TRX',
            'USDT',
            'ETC',
            'BTG',
            'QTUM',
            'VEN',
            'ZEC',
            'ICX',
            'OMG',
            'XRB',
            'STEEM',
            'PPT',
            'BNB',
            'BCN',
            'SNT',
            'XVG',
            'SC',
            'STRAT',
            'MKR',
            'BTS',
            'AE',
            'REP',
            'DOGE',
            'VERI',
            'WAVES',
            'WTC',
            'DCR',
            'ARDR',
            'ZRX',
            'RHOC',
            'HSR',
            'KCS',
            'DGD',
            'R',
            'KMD',
            'KNC',
            'ETN',
            'ARK',
            'GAS',
            'LRC',
            'BTM',
            'DCN',
            'BAT',
            'DGB',
            'ZIL',
            'DRGN',
            'GBYTE',
            'PIVX',
            'ZCL',
            'CNX',
            'ELF',
            'QASH',
            'BTX',
            'ETHOS',
            'GXS',
            'NAS',
            'GNT',
            'SYS',
            'PLR',
            'POWR',
            'IOST',
            'FUN',
            'DENT',
            'CND',
            'MONA',
            'FCT',
            'KIN',
            'SALT',
            'SMART',
            'XZC',
            'BNT',
            'AION',
            'PART',
            'ENG',
            'NXT',
            'RDD',
            'MAID',
            'PAY',
            'IGNIS',
            'QSP',
            'AGI',
            'REQ',
            'XP',
            'NXS',
            'WAX',
            'XPA',
            'ICN',
            'GNO',
            'EMC',
            'SUB',
            'GAME',
            'XDN',
            'UCASH',
            'LINK',
            'NEBL',
            'CVC',
            'BLOCK',
            'VTC',
            'BTCD',
            'HPB',
            'STORJ',
            'SKY',
            'RDN',
            'MANA',
            'ECN',
            'POE',
            'DEW',
            'UNITY',
            'ACT',
            'TNB',
            'MED',
            'NAV',
            'ANT',
            'ZEN',
            'STORM',
            'ENJ',
            'HTML',
            'DTR',
            'RLC',
            'SAN',
            'UBQ',
            'PPP',
            'SRN',
            'VEE',
            'AGRS',
            'BLZ',
            'BCO',
            'MCO',
            'EMC2',
            'VIBE',
            'C20',
            'SPHTX',
            'BIX',
            'ITC',
            'JNT',
            'PPC',
            'XAS',
            'RPX',
            'SNGLS',
            'MDS',
            'LEND',
            'RCN',
            'AST',
            'COB',
            'PAC',
            'CMT',
            'SNM',
            'XBY',
            'DBC',
            'ADX',
            'SPANK',
            'XCP',
            'AMB',
            'MTL',
            'OST',
            'TEL',
            'UTK',
            'BAY',
            'QRL',
            'PRL',
            'EDG',
            'THETA',
            'MGO',
            'WABI',
            'NLG',
            'VIA',
            'MLN',
            'TNC',
            'WGR',
            'INS',
            'DATA',
            'APPC',
            'UKG',
            'MOD',
            'TRIG',
            'TNT',
            'EDO',
            'CDT',
            'ION',
            'WINGS',
            'NULS',
            'ETP',
            'CTR',
            'NGC',
            'ECA',
            'ATM',
            'GVT',
            'SOC',
            'FUEL',
            'LBC',
            'MER',
            'MNX',
            'LKK',
            'IDH',
            'BURST',
            'ECC',
            'INT',
            'QLC',
            'CRW',
            'SLS',
            'DNT',
            'BRD',
            'AEON',
            'CLOAK',
            'HVN',
            'ADT',
            'TSL',
            'GRS',
            'DCT',
            'TRAC',
            'COSS',
            'TAAS',
            'HST',
            'CAPP',
            'CV',
            'ONION',
            'DAT',
            'TKN',
            'SAFEX',
            'PURA',
            'OCN',
            'PRE',
            '1ST',
            'SBD',
            'GTO',
            'VIB',
            'LUN',
            'INK',
            'QBT',
            'FTC',
            'BDG',
            'BITCNY',
            'THC',
            'IOC',
            'NMC',
            'YOYOW',
            'DPY',
            'XWC',
            'SHIFT',
            'XSPEC',
            'HMQ',
            'PEPECASH',
            'DMD',
            'CFI',
            'POT',
            'SWFTC',
            'TRST',
            'NET',
            'VOX',
            'DIME',
            'IPL',
            'SIB',
            'TIX',
            'TAU',
            'UNO',
            'MTH',
            'LOCI',
            'ZSC',
            'BLT',
            'FLASH',
            'IXT',
            'TIO',
            'RISE',
            'KRM',
            'MOON',
            'POSW',
            'SNC',
            'AMP',
            'LEO',
            'WRC',
            'EVX',
            'CAT',
            'LA',
            'FAIR',
            'VRC',
            'PASC',
            'ORME',
            'MOT',
            'COLX',
            'PHR',
            'KEY',
            'XSH',
            'NEU',
            'AURA',
            'MDA',
            'DLT',
            'DRT',
            'GUP',
            'PRO',
            'NLC2',
            'PLC',
            'OTN',
            'XEL',
            'NVST',
            'BLK',
            'GRC',
            'QUN',
            'NMR',
            'BITB',
            'GTC',
            'SOAR',
            'EXP',
            'BOT',
            'MYB',
            'CAN',
            'COV',
            'HGT',
            'BBR',
            'UNIT',
            'HKN',
            'ZOI',
            'BCPT',
            'RADS',
            'AIR',
            'PKT',
            'PPY',
            'DNA',
            'SLR',
            'ARN',
            'SWT',
            'OK',
            'MSP',
            'NSR',
            'OMNI',
            'STX',
            'UQC',
            'SNOV',
            'ENRG',
            'DICE',
            'PUT',
            'WCT',
            'GOLOS',
            'MUE',
            'RBY',
            'NYC',
            'OXY',
            'BSD',
            'XMY',
            'BMC',
            'HOT',
            'KICK',
            'EDR',
            'BITUSD',
            'XNN',
            'EBTC',
            'MEE',
            'PST',
            'PRG',
            'OAX',
            'ICOS',
            'GBX',
            'XAUR',
            'VOISE',
            'LOC',
            'PLBT',
            'CLAM',
            'POLL',
            'BNTY',
            'OCT',
            'ATB',
            'NXC',
            'BLUE',
            'ECOB',
            'CSNO',
            'NEOS',
            'USNBT',
            'LMC',
            'XPM',
            'DBET',
            'RVT',
            'VIU',
            'PRA',
            'DAI',
            'GET',
            'LUX',
            'MINT',
            'XUC',
            'QAU',
            'TIME',
            'AUR',
            'INCNT',
            'RNT',
            'ALIS',
            'AIT',
            'GAM',
            'BPT',
            'FLO',
            'GAT',
            'DBIX',
            'PND',
            'FLDC',
            'DTB',
            'TIPS',
            'IFT',
            'PTOY',
            'AVT',
            'HDG',
            'XLR',
            'GCR',
            'RMC',
            'MYST',
            'PLU',
            'PIRL',
            'DYN',
            'BQ',
            'SYNX',
            'HAC',
            'DIVX',
            'OBITS',
            'COVAL',
            'PZM',
            'ODN',
            'ELIX',
            'LIFE',
            'ESP',
            'SEQ',
            'HORSE',
            'XRL',
            'POLIS',
            'NTRN',
            'DOVU',
            'LEV',
            'MUSIC',
            'SPF',
            'HAT',
            'BIS',
            'LINDA',
            'CAT',
            'BCY',
            'NIO',
            'XST',
            'SXUT',
            'XTO',
            'RC',
            'CURE',
            'DRP',
            'ABY',
            'EVR',
            'ARY',
            'BWK',
            'FLIXX',
            'CAG',
            'SPHR',
            'IOP',
            'DOPE',
            'PARETO',
            'CVCOIN',
            'PINK',
            'EAC',
            'PBL',
            'ING',
            'BTCZ',
            'AIX',
            'ALQO',
            'XVC',
            'SPRTS',
            'PIX',
            'XMCC',
            'TOA',
            'SUMO',
            'NVC',
            'AC',
            '1337',
            'PFR',
            'B2B',
            'HEAT',
            'ERO',
            'UFO',
            'WISH',
            'MEME',
            'HYP',
            'TIE',
            'VRM',
            'GCN',
            'SSS',
            'CRED',
            'QWARK',
            'HUSH',
            'BTM',
            'FLIK',
            'PLAY',
            'ERC',
            'ADST',
            'DOT',
            'ATMS'
        ]
        self.tempInvalidCoins = ['BTG','BLZ']
        for invalidCoin in self.tempInvalidCoins:
            self.coins.remove(invalidCoin)
        self.ETHBTC = ccxt.coinmarketcap().fetch_ticker("ETH/USD")['info']['price_btc']
    def upDateETHBTC(self):
        try:
            self.ETHBTC = ccxt.coinmarketcap().fetch_ticker("ETH/USD")['info']['price_btc']
        except:
            print('ETHBTC did not update')
            pass
    def updateExchanges(self):
        for exchange in self.exchanges:
            exchange.updateMarkets()

    def findMargins(self):
        self.updateExchanges()
        self.upDateETHBTC()
        coinDict = {}
        for coin in self.coins:
            low = 10000000
            lowExchange = ''; askBase = ''; bidBase = ''
            high = 0
            highExchange = ''
            for exchange in self.exchanges:
                low,high,lowExchange,highExchange,bidBase,askBase = self.updateSymbolAttributes(exchange,coin,low,high,lowExchange,highExchange,bidBase,askBase)
            if high/low > 1.01:
                coinMargin = {'bid': low,'bidExchange': lowExchange,"bidBase":bidBase,'ask':high,'askExchange':highExchange,'askBase':askBase,'margin': float(high/low)}
                orders = self.calculateProfit(coin,bidBase,askBase,coinMargin)
                try:
                    transactionFee = coinMargin['bidExchange'].fees['funding']['withdraw'][coin]*low
                except:
                    transactionFee = -1
                if orders['buys'] != [] and transactionFee != -1:
                    profit = 0
                    volume = 0
                    ethPrice = ''
                    for i in orders['buys']:
                        profit += i[2]
                        volume += i[1]
                    if profit-transactionFee > 0:
                        coinDict[coin] = coinMargin
                        print(coin + " Buy from: " + coinMargin['bidExchange'].id + " for " + bidBase + " | Sell to: " +
                              coinMargin['askExchange'].id + " for " + askBase)
                        for i in range(len(orders['buys'])):
                            if bidBase == "ETH":
                                ethPrice = " -> " + str(orders['buys'][i][0]/self.ETHBTC)
                            print("Buy: " + str(orders['buys'][i][1]) + " @" + str(orders['buys'][i][0]) + ethPrice)
                            if askBase == "ETH":
                                ethPrice = " -> " + str(orders['sells'][i][0]/self.ETHBTC)
                            print("Sell: " + str(orders['sells'][i][1]) + " @" + str(orders['sells'][i][0]) + ethPrice)
                        print('For total volume of ' + str(volume) + " and profit of " + str(profit) + "\n")
        if coinDict == {}:
            print("No orders")

    def calculateProfit(self,coin,bidBase,askBase,margin):
        orders = {'buys': [],'sells': []}
        try:
            sellOrders = margin['bidExchange'].fetch_order_book(coin + "/" + bidBase)['asks']
        except:
            return orders
        if bidBase == "ETH":
            for i in range(len(sellOrders)): sellOrders[i][0] *= self.ETHBTC
        low = margin['bid']; profit = 0
        try:
            buyOrders = margin['askExchange'].fetch_order_book(coin + "/" + askBase)['bids']
        except:
            return orders
        if askBase == "ETH":
            for i in range(len(buyOrders)): buyOrders[i][0] *= self.ETHBTC
        high = margin['ask']; tradeMargin = margin['margin']
        while sellOrders != [] and buyOrders != [] and sellOrders[0][0] < low*tradeMargin and buyOrders[0][0] > high*(1-tradeMargin):
            tradeVol = min(sellOrders[0][1],buyOrders[0][1])
            fees = tradeVol*(sellOrders[0][0]*margin['bidExchange'].fees['trading']['taker'] + buyOrders[0][0]*margin['askExchange'].fees['trading']['taker'])
            sellOrders[0][1] -= tradeVol
            buyOrders[0][1] -= tradeVol
            profit = tradeVol*(buyOrders[0][0] - sellOrders[0][0]) - fees
            if profit > 0:
                orders['buys'].append([sellOrders[0][0], tradeVol*sellOrders[0][0],profit])
                orders['sells'].append([buyOrders[0][0], tradeVol*buyOrders[0][0],profit])
            else:
                break
            if sellOrders[0][1] == 0:
                sellOrders = sellOrders[1:]
            if buyOrders[0][1] == 0:
                buyOrders = buyOrders[1:]
        return orders



    def updateSymbolAttributes(self,exchange,coin,low,high,lowExchange,highExchange,askBase,bidBase):
        if exchange.isSybmolInMarket(coin,"BTC"):
            market = exchange.getSymbolMarket(coin,"BTC")
            try:
                if low > market['ask'] and exchange.has['withdraw']:
                    low = market['ask'];lowExchange = exchange;bidBase="BTC"
                if high < market['bid'] and exchange.has['deposit']:
                    high = market['bid'];highExchange = exchange;askBase="BTC"
            except:
                pass
        if exchange.isSybmolInMarket(coin,"ETH"):
            market = exchange.getSymbolMarket(coin,"ETH")
            try:
                if low > market['ask']*self.ETHBTC and exchange.has['withdraw']:
                    low = market['ask']*self.ETHBTC
                    lowExchange = exchange;bidBase="ETH"
                if high < market['bid']*self.ETHBTC and exchange.has['deposit']:
                    high = market['bid']*self.ETHBTC
                    highExchange = exchange;askBase="ETH"
            except:
                pass
        return low, high,lowExchange,highExchange,bidBase,askBase

arb = arbitrage()
for i in range(100):
    arb.findMargins()
    time.sleep(10)
    print('\n')
