import pandas
from statistics import stdev
import numpy as np
import matplotlib.pyplot as plt
import ccxt
import time


exchange = ccxt.gdax({
    'rateLimit': 10000,
    'enableRateLimit': True,
    'verbose': False,
})


buying = False
collection_size = 50  # decides the size of the samples taken to calculate the avg and stdev
curr_accept_price = None
percent_gain = 1.002
curr_buy_order_price = None
last_points = []


while True:
    if len(last_points) < collection_size:
        print(len(last_points))
        ticker = exchange.fetch_ticker('BTC/USD')
        current_price = ticker['last']
        last_points.append(current_price)
        if len(last_points) == collection_size:
            buying = True
            print('Buying')
            print('-' * 30)
        time.sleep(5)
    if buying:
        ticker = exchange.fetch_ticker('BTC/USD')
        current_price = ticker['last']
        curr_avg = sum(last_points) / len(last_points)
        curr_std = stdev(last_points)
        if curr_avg - (1.5*curr_std) > current_price:

            if curr_avg - (1.5*curr_std) == curr_buy_order_price:
                print('Buy order of ' + str(curr_buy_order_price) + ' remains.')
            else:
                curr_buy_order_price = curr_avg - (1.5 * curr_std)
                print(f'Create temporary buy order at -- {curr_buy_order_price}')

        else:
            last_points.append(current_price)
            del last_points[0]
            print(f'Price is not lower than {curr_avg - (1.5*curr_std)}')
        time.sleep(60)
    # if selling:
    #     ticker = exchange.fetch_ticker('BTC/USD')
    #     curr_price = ticker['last']
    #     if curr_price > (buy_point*percent_gain):
    #




