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

#grab Scryfall price data
file1 = open('ScryfallPriceData.json')
data1 = json.load(file1)
file1.close()

#establish dicts for buy candidates and sell candidates
sell_cans = {}
buy_cans = {}

#pick the number of days to perform analysis on
x = 60

#grab prices for each card and calculate the z score
for card, dates in data1.items():
    price_list = [price for price in dates.values()]
    prices = [float(price) for price in price_list]
    prices = prices[-x:]
    avg = stats.mean(prices)
    std = stats.stdev(prices)
    try:
        zscore = (prices[-1]-avg)/std
    except ZeroDivisionError:
        zscore = 0
    #if the zscore is above/below two std devs, add to the proper candidate list
    if zscore > 1.96:
        sell_cans[card] = zscore
    if zscore < -1.96:
        buy_cans[card] = zscore

#print the buy and sell candidates according to the Scryfall data
print('Scryfall data:')
print(f'Sell candidates- {sell_cans}')
print('\n')
print(f'Buy candidates- {buy_cans}')

#begin same process for MTGO Collection prices
file2 = open('MTGOCollectionPrices.json')
data2 = json.load(file2)
file2.close()

sell_cans = {}
buy_cans = {}

for card, dates in data2.items():
    date_list, price_list = [date for date in dates.keys()], [price for price in dates.values()]
    last_date = date_list[-1].split('-')
    last_date_formatted = date(int(last_date[-1]), int(last_date[0]), int(last_date[1]))
    delta = today - last_date_formatted
    prices = [float(price) for price in price_list]
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
        sell_cans[card] = zscore
    if zscore < -1.96 and delta.days < 10:
        buy_cans[card] = zscore

print('\n')
print('Cardhoarder data:')
print(f'Sell candidates- {sell_cans}')
print('\n')
print(f'Buy candidates- {buy_cans}')