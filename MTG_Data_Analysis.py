#!/usr/bin/env python3

import json
import statistics as stats

# import Cardhoarder_Scraper
# import Scryfall_API

file1 = open('MTGPriceData.json')
data = json.load(file1)
file1.close()

sellcans = {}
buycans = {}

x = 60

for card, dates in data.items():
    pricelist = [price for price in dates.values()]
    prices = [float(price) for price in pricelist]
    prices = prices[-x:]
    avg = stats.mean(prices)
    std = stats.stdev(prices)
    try:
        zscore = (prices[-1]-avg)/std
    except ZeroDivisionError:
        zscore = 0
    if zscore > 1.96:
        sellcans[card] = zscore
    if zscore < -1.96:
        buycans[card] = zscore
    # print(prices, avg, std, zscore)

print('Scryfall data:')
print(f'Sell candidates- {sellcans}')
print(f'Buy candidates- {buycans}')

file1 = open(r'C:\Users\allst\Documents\!Python\Programs\Selenium\MTGOCollectionPrices.json')
data2 = json.load(file1)
file1.close()

sellcans = {}
buycans = {}

for card, dates in data2.items():
    pricelist = [price for price in dates.values()]
    prices = [float(price) for price in pricelist]
    prices = prices[-x:]
    avg = stats.mean(prices)
    if len(prices) > 1:
        std = stats.stdev(prices)
    else:
        pass
    try:
        zscore = (prices[-1] - avg) / std
    except ZeroDivisionError:
        zscore = 0
    if zscore > 1.96:
        sellcans[card] = zscore
    if zscore < -1.96:
        buycans[card] = zscore

print('\n')
print('Cardhoarder data:')
print(f'Sell candidates- {sellcans}')
print(f'Buy candidates- {buycans}')
