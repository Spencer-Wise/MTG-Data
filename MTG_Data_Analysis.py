#!/usr/bin/env python3

import json
import statistics as stats
from datetime import datetime
from datetime import date

import Cardhoarder_Scraper
import Scryfall_API

print('\n')

today = datetime.now().date()
# randomdate = date(2020, 1, 5)

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

print('Scryfall data:')
print(f'Sell candidates- {sellcans}')
print('\n')
print(f'Buy candidates- {buycans}')

file2 = open('MTGOCollectionPrices.json')
data2 = json.load(file2)
file2.close()

sellcans = {}
buycans = {}

for card, dates in data2.items():
    datelist, pricelist = [date for date in dates.keys()], [price for price in dates.values()]
    lastdate = datelist[-1].split('-')
    lastdateformatted = date(int(lastdate[-1]), int(lastdate[0]), int(lastdate[1]))
    delta = today - lastdateformatted
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
    if zscore > 1.96 and delta.days < 10:
        sellcans[card] = zscore
    if zscore < -1.96 and delta.days < 10:
        buycans[card] = zscore

print('\n')
print('Cardhoarder data:')
print(f'Sell candidates- {sellcans}')
print('\n')
print(f'Buy candidates- {buycans}')