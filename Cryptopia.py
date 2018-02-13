import math
import time
import re
from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
import ccxt

class cryptopia (ccxt.cryptopia):

    def __init__(self):
        super().__init__()
        self.childMarkets = {}
        self.fees['trading']['maker'] = 0.002
        self.fees['trading']['taker'] = 0.002
        self.has['deposit'] = False
        self.fees['funding']['withdraw'] = {
            'BTC': 0.00100000,
            'ETH': 0.00500000,
            'BCH': 0.00080000,
            'LTC': 0.02000000,
            'NEO': 0.00000000,
            'XEM': 1.00000000,
            'DASH': 0.01000000,
            'XMR': 0.02800000,
            'TRX': 0.01000000,
            'USDT': 40.00000000,
            'ETC': 0.01000000,
            'BTG': 0.01000000,
            'QTUM': 0.05000000,
            'ZEC': 0.00020000,
            'OMG': 0.20000000,
            'XVG': 1.00000000,
            'STRAT': 0.01000000,
            'REP': 0.06000000,
            'DOGE': 3.00000000,
            'DCR': 0.03000000,
            'HSR': 0.01000000,
            'R': 5.00000000,
            'KMD': 0.01000000,
            'KNC': 1.50000000,
            'ETN': 10.00000000,
            'ARK': 0.10000000,
            'BTM': 14.00000000,
            'DCN': 1000.00000000,
            'BAT': 0.00010000,
            'DGB': 0.50000000,
            'GBYTE': 0.00002000,
            'PIVX': 0.01000000,
            'ZCL': 0.01000000,
            'BTX': 0.01000000,
            'GNT': 6.00000000,
            'PLR': 9.00000000,
            'POWR': 0.01000000,
            'FCT': 0.10000000,
            'SMART': 0.01000000,
            'XZC': 0.01000000,
            'RDD': 0.50000000,
            'MAID': 29.00000000,
            'PAY': 1.00000000,
            'NXS': 0.15000000,
            'GNO': 0.01600000,
            'EMC': 0.03000000,
            'GAME': 0.00010000,
            'NEBL': 0.01000000,
            'BTCD': 0.00010000,
            'SKY': 0.00000000,
            'NAV': 0.00010000,
            'ZEN': 0.01000000,
            'ENJ': 50.00000000,
            'UBQ': 0.01000000,
            'BLZ': 10.00000000,
            'EMC2': 0.01000000,
            'PPC': 0.00010000,
            'PAC': 100.00000000,
            'CMT': 0.01000000,
            'XBY': 1.00000000,
            'SPANK': 0.01000000,
            'MTL': 0.40000000,
            'BAY': 0.01000000,
            'PRL': 0.01000000,
            'MGO': 4.00000000,
            'CTR': 6.00000000,
            'FUEL': 0.01000000,
            'LBC': 0.01000000,
            'CLOAK': 0.01000000,
            'GRS': 0.01000000,
            'HST': 8.00000000,
            'CAPP': 0.01000000,
            'ONION': 0.01000000,
            'SAFEX': 1500.00000000,
            'PURA': 0.01000000,
            'QBT': 0.01000000,
            'FTC': 1.00000000,
            'NMC': 0.00010000,
            'XSPEC': 0.01000000,
            'NET': 0.00010000,
            'DIME': 0.00010000,
            'SIB': 0.01000000,
            'TIX': 2.00000000,
            'UNO': 0.01000000,
            'FLASH': 0.01000000,
            'POSW': 0.01000000,
            'AMP': 44.00000000,
            'WRC': 0.01000000,
            'CAT': 0.00010000,
            'VRC': 0.00010000,
            'PASC': 0.01000000,
            'ORME': 1.00000000,
            'PHR': 0.01000000,
            'NLC2': 0.01000000,
            'PLC': 0.00010000,
            'OTN': 0.20000000,
            'BLK': 0.00010000,
            'BITB': 0.00010000,
            'EXP': 0.01000000,
            'MYB': 1.00000000,
            'CAN': 0.01000000,
            'BBR': 0.10000000,
            'UNIT': 0.01000000,
            'ZOI': 0.01000000,
            'BCPT': 14.00000000,
            'DNA': 5.00000000,
            'OK': 0.00500000,
            'MSP': 22.00000000,
            'NSR': 100.00000000,
            'PUT': 0.01000000,
            'RBY': 0.00010000,
            'BSD': 0.00500000,
            'XMY': 0.00010000,
            'GBX': 0.01000000,
            'VOISE': 245.00000000,
            'CLAM': 0.00010000,
            'POLL': 1.50000000,
            'ECOB': 0.01000000,
            'USNBT': 5.00000000,
            'XPM': 0.00010000,
            'DBET': 21.00000000,
            'LUX': 0.01000000,
            'MINT': 0.00010000,
            'AUR': 0.00010000,
            'ALIS': 5.00000000,
            'DBIX': 0.04000000,
            'PND': 10.00000000,
            'IFT': 50.00000000,
            'XLR': 0.01000000,
            'PIRL': 0.01000000,
            'SYNX': 0.01000000,
            'HAC': 38.00000000,
            'DIVX': 3.00000000,
            'ODN': 0.01000000,
            'NTRN': 0.10000000,
            'MUSIC': 0.01000000,
            'BIS': 0.02000000,
            'LINDA': 0.01000000,
            'CAT': 0.00010000,
            'XST': 0.01000000,
            'RC': 1.00000000,
            'DRP': 5.00000000,
            'ABY': 0.01000000,
            'EVR': 2.00000000,
            'BWK': 0.01000000,
            'DOPE': 0.01000000,
            'PINK': 0.01000000,
            'PBL': 12.00000000,
            'XMCC': 0.01000000,
            'TOA': 0.01000000,
            'SUMO': 0.01000000,
            'NVC': 0.00010000,
            'AC': 1.00000000,
            '1337': 0.01000000,
            'HEAT': 0.01000000,
            'WISH': 0.01000000,
            'HYP': 1.00000000,
            'VRM': 0.01000000,
            'GCN': 100.00000000,
            'QWARK': 0.01000000,
            'HUSH': 0.01000000,
            'BTM': 14.00000000,
            'ADST': 7.00000000,
            'DOT': 0.00000000,
            'ATMS': 0.01000000}


    def updateMarkets(self):
        marketsJson = self.fetch_tickers()
        for market in marketsJson:
            market = marketsJson[market]['info']
            self.childMarkets[market['Label']] = {
                'bid': float(market['BidPrice']),
                'ask': float(market['AskPrice'])}

    def getSymbolMarket(self,symbol,base):
        try:
            return self.childMarkets[symbol+ "/" +base]
        except:
            return None

    def isSybmolInMarket(self, symbol, base):
        try:
            self.childMarkets[symbol + "/" + base]
            return True
        except:
            return False