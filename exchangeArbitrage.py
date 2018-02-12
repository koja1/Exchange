import math
import time
import re
from bs4 import BeautifulSoup
import requests
import json
import Exchange.Binance
import Exchange.Kucoin


class arbitrage():

    def __init__(self):
        self.exchanges = [
            Exchange.Binance.binance(),
            Exchange.Kucoin.kucoin()
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
            'BCC',
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
        self.ETHBTC = float(json.loads(BeautifulSoup(requests.get("https://api.coinmarketcap.com/v1/ticker/ethereum/").content,"html.parser").prettify())[0]['price_btc'])

    def upDateETHBTC(self):
        self.ETHBTC = float(json.loads(BeautifulSoup(requests.get("https://api.coinmarketcap.com/v1/ticker/ethereum/").content,"html.parser").prettify())[0]['price_btc'])

    def updateExchanges(self):
        for exchange in self.exchanges:
            exchange.updateMarkets()
    def findMargins(self):
        self.updateExchanges()
        self.upDateETHBTC()
        coinDict = {}
        for coin in self.coins:
            low = 10000000
            lowExchange = ''
            high = 0
            highExchange = ''
            for exchange in self.exchanges:
                low,high,lowExchange,highExchange = self.updateSymbolAttributes(exchange,coin,low,high,lowExchange,highExchange)
            if high/low > 1.01:
                coinMargin = {'bid': low,'bidExchange': lowExchange,'ask':high,'askExchange':highExchange,'margin': float(high/low)}
                if self.validateMargin(coinMargin):
                    coinDict[coin] = coinMargin

    def validateMargin(self,margin):
        pass
    
    def updateSymbolAttributes(self,exchange,coin,low,high,lowExchange,highExchange):
        if exchange.isSybmolInMarket(coin,"BTC"):
            market = exchange.getSymbolMarket(coin,"BTC")
            try:
                if low > market['ask']:
                    low = market['ask']
                    lowExchange = exchange.id
                if high < market['bid']:
                    high = market['bid']
                    highExchange = exchange.id
            except:
                pass
        if exchange.isSybmolInMarket(coin,"ETH"):
            market = exchange.getSymbolMarket(coin,"ETH")
            try:
                if low > market['ask']*self.ETHBTC:
                    low = market['ask']*self.ETHBTC
                    lowExchange = exchange.id + "|e"
                if high < market['bid']*self.ETHBTC:
                    high = market['bid']*self.ETHBTC
                    highExchange = exchange.id + "|e"
            except:
                pass
        return low, high,lowExchange,highExchange

arb = arbitrage()
for i in range(100):
    arb.findMargins()
    time.sleep(10)
    print('\n')
