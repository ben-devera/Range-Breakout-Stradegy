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
selling = False
recollecting = False
collection_size = 30  # decides the size of the samples taken to calculate the avg and stdev
curr_accept_price = None
percent_gain = 1.002
curr_buy_order_price = None
last_points = []
simulation_money = 10000
coin_tracker = 0
last_sell = 0
last_sell_max = 15
last_buy = 0
last_buy_max = 15


while True:
    if len(last_points) < collection_size:
        print(len(last_points))
        ticker = exchange.fetch_ticker('BTC/USD')
        current_price = ticker['last']
        last_points.append(current_price)
        if len(last_points) == collection_size:
            buying = True
            print('Looking to buy')
            print('-' * 50)
        time.sleep(5)

    elif recollecting:
        for i in range(30):
            ticker = exchange.fetch_ticker('BTC/USD')
            current_price = ticker['last']
            last_points.append(current_price)
            del last_points[0]
            time.sleep(5)

        recollecting = False
        buying = True
        print('Looking to buy')
        print('-'*50)

    elif buying:
        if last_buy == last_buy_max:
            buying = False
            recollecting = True
            last_buy = 0
            print('Recollecting')
            print('-'*50)
        else:
            ticker = exchange.fetch_ticker('BTC/USD')
            current_price = ticker['last']
            curr_avg = sum(last_points) / len(last_points)
            curr_std = stdev(last_points)
            if curr_avg - (1.5*curr_std) >= current_price:

                curr_buy_order_price = curr_avg - (1.5 * curr_std)
                print(f'Create temporary buy order at -- {curr_buy_order_price}')
                coin_tracker = simulation_money / current_price
                print(f'{coin_tracker} coins purchased.')
                selling = True
                buying = False
                print('Looking for point to sell')
                print('-'*50)

            else:
                last_points.append(current_price)
                del last_points[0]
                print(f'Price is not lower than {curr_avg - (1.5*curr_std)}')
                last_buy += 1

            time.sleep(60)

    elif selling:
        ticker = exchange.fetch_ticker('BTC/USD')
        curr_price = ticker['last']
        curr_accept_price = curr_buy_order_price * percent_gain

        if last_sell == last_sell_max:
            curr_accept_price = curr_accept_price * .98
            last_sell -= 1

        if curr_price > curr_accept_price:
            simulation_money = coin_tracker * curr_price
            print(f'Create Temporary sell order at -- {curr_price}')
            print(f'Current value of investment is ${simulation_money}')
            selling = False
            recollecting = True
            last_sell = 0
            print('Recollecting')
            print('-'*50)

        else:
            last_sell += 1

        time.sleep(15)





