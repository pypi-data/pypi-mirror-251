import numpy as np
from talib.abstract import *

def macd(data, fastperiod=12, slowperiod=26, signalperiod=9):
    if isinstance(data, list):
        macd, macdsignal, macdhist = MACD(np.array(data, dtype='double'), fastperiod, slowperiod, signalperiod)
        return macd

def ma(data, timeperiod=12):
    if isinstance(data, list):
        ma5 = SMA(np.array(data, dtype='double'), timeperiod)
        return ma5

def rsi(data):
    if isinstance(data, list):
        rsi = RSI(np.array(data, dtype='double'))
        return rsi


if __name__ == '__main__':
    print("test")