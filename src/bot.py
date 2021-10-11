import pandas as pd
import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
from src.config import API_KEY, API_SECRET

SOCKET = "wss://stream.binance.us:9443/ws/algousd@kline_1m"

TRADE_SYMBOL = 'ALGOUSD'
TRADE_QUANTITY = 25

closes = []
lows = []
highs = []
opens = []
volumes = []
trades_qty = []
l_of_l = []
symbols = []
df = pd.DataFrame()

in_position = False

client = Client(API_KEY, API_SECRET, tld='us')


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True


def on_open(ws):
    print('opened connection')


def on_close(ws):
    print('closed connection')


def on_message(ws, message):
    global closes, in_position, lows, highs, last_high, previous_high, last_low, previous_low, opens, volumes, trades_qty, l_of_l, symbols, df
    json_message = json.loads(message)
    candle = json_message['k']
    ticker = candle['s']
    is_candle_closed = candle['x']
    open = candle['o']
    volume = candle['v']
    num_of_trades = candle['n']
    low = candle['l']
    high = candle['h']
    close = candle['c']

    if is_candle_closed:
        pprint.pprint("candle closed at {}".format(close))
        closes.append(float(close))
        lows.append(float(low))
        highs.append(float(high))
        opens.append((float(open)))
        volumes.append((float(volume)))
        trades_qty.append((float(num_of_trades)))
        symbols.append(ticker)
        l_of_l = [symbols, closes, lows, highs, opens, volumes, trades_qty]
        df = pd.DataFrame(l_of_l).T
        df.columns = ['Ticker', 'Close', 'Low', 'High', 'Open', 'Volume', "Qty of Trades"]
        df.to_csv(index=False)



ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
