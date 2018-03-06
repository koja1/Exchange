import Binance

binance = Binance.binance()

binance.apiKey = ''
binance.secret = ''
coins = [
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
dict = {}
for coin in coins:
    dict[coin] = {'buyQ': 0,'buyC': 0,'sellQ': 0,'sellC': 0,'profit': 0,'trades': 0}
for coin in coins:
    trades = binance.fetch_closed_orders(coin+"/BTC",1520293482565-6.048e+8)
    buyQ = 0
    buyC = 0
    sellQ = 0
    sellC = 0
    dict[coin]['trades'] = len(trades)
    for trade in trades:
        if trade['side'] == "buy":
            buyQ += trade['amount']
            buyC += trade['cost']
        elif trade['side'] == 'sell':
            sellQ += trade['amount']
            sellC += trade['cost']
    if buyQ > sellQ:
        buyC = buyC*sellQ/buyQ
        buyQ = sellQ
    elif sellQ > buyQ:
        sellC = sellC*buyQ/sellQ
        sellQ = buyQ
    dict[coin]['buyQ'] = buyQ
    dict[coin]['buyC'] = buyC
    dict[coin]['sellQ'] = sellQ
    dict[coin]['sellC'] = sellC
    dict[coin]['profit'] = sellC-buyC

for coin in coins:
    if dict[coin]['profit'] <= 0:
        print("'" + coin + "',")
        qty = binance.fetch_free_balance()[coin]
        if qty*binance.fetch_order_book(coin + '/BTC')['bids'][0][0] > 0.001:
            binance.create_market_sell_order(coin+"/BTC",qty)