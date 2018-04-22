import pandas
from statistics import stdev
import numpy as np
import matplotlib.pyplot as plt

file = '/Users/bendevera/PycharmProjects/masterSteve/gdax_april10_april19.csv'
file1 = '/Users/bendevera/PycharmProjects/masterSteve/gdax_april1_april20.csv'
file2 = '/Users/bendevera/PycharmProjects/masterSteve/gdax_jan1_april20.csv'
names = ['time', 'open', 'high', 'low', 'close', 'volume']
data = pandas.read_csv(file2, header=None, names=names)

initial_investment = 10000  # initial investment can use "input('how large is the investment:')" for user input
investment = initial_investment  # will equal final value of investment after all trades
investment_log = []  # tracks value of investment over the whole trading period
coins = 0  # keeps track of number of coins owned at any given time
coin_log = []  # logs all coin values from all transactions
granularity = 5  # time span of each fetched data point
time_elapsed = ((len(data) * granularity) / 60) / 24   # days since trading started
collection = []  # set of data used to create the sample avg and stdev
collection_size = 15  # decides the size of the samples taken to calculate the avg and stdev
buypoints = []  # all points where buy was made
sellpoints = []  # all points where sell was made
returns = []  # all returns made from each buy/sell

collecting = True
buying = False
selling = False

counter = 0  # current place of for loop

last_sell = 0  # number of checks since buy was made
last_sell_max = 10  # will automatically sell if last sell is equal to this value// time is value * granularity
curr_accept_price = None
curr_sell_point = None

last_collect = 0  # number of checks since collectio was made
last_collect_max = 15  # will automatically recollect collection if last collect equal to this value


for elem in data['high'].values:
    if collecting:
        collection.append(elem)
        if len(collection) == collection_size:
            collecting = False
            buying = True
    #  while collecting: appends each successive point to collection till collection is 10 points

    elif buying:
        curr_avg = sum(collection) / len(collection)
        curr_std = stdev(collection)
        if elem < (curr_avg - (1.5 * curr_std)):
            buy_point = [elem, counter]
            curr_accept_price = elem
            coins = investment / elem
            coin_log.append(coins)
            buypoints.append(buy_point)
            buying = False
            selling = True
        elif last_collect > last_collect_max:
            collection = []
            last_collect = 0
            buying = False
            collecting = True
        else:
            last_collect += 1
    #  while buying: checks each point for price to enter, if point isn't found in last_collect_max,
    #  collection is set to empty array and recollected. If point is found, buy is made and process is sent to
    #  selling mode

    elif selling:
        if curr_accept_price > (buy_point[0] * 1.002) or last_sell == last_sell_max:
            sell_point = [elem, counter]
            investment = coins * elem
            coins = 0
            curr_return = sell_point[0] - buy_point[0]
            returns.append(curr_return)
            sellpoints.append(sell_point)
            collecting = True
            selling = False
            collection = []
            last_sell = 0
        else:
            if last_sell%2 == 0:
                curr_accept_price = elem
            last_sell += 1
    #  while selling: checks each point for price to sell at, if point is found or isn't found in last_sell_max
    #  points, sale is made and process is set back to collecting

    if investment != 0:
        investment_log.append(investment)
    else:
        investment_log.append(coins*elem)
    counter += 1


growth = ((investment / initial_investment) - 1) * 100

# Makes plot that graphs (time,value_of_investment)
X = np.linspace(0, len(investment_log), len(investment_log), endpoint=True)
plt.plot(X, investment_log)

ticks = []
for i in range(int(time_elapsed)):
    ticks.append(i)
# Set x ticks
# plt.xticks(location_lst, label_list)

# Set y limits
# plt.ylim(-1.0,1.0)

plt.show()

# Makes plot of the high values of btc over the time period being evaluated
Y = np.linspace(0, len(data['high'].values), len(data['high'].values), endpoint=True)
plt.plot(Y, data['high'].values)

plt.show()

print(f"Initial investment was ${initial_investment}")
print(f"Value of investment after trades is {investment} after {time_elapsed} days of trading.")
print(f"Growth is {growth}%")
print(f"Total returns is ${sum(returns)}")
