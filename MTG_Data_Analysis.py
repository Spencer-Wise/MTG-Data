#!/usr/bin/env python3

import json
import statistics as stats
from datetime import datetime
from datetime import date
import tkinter as tk

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
scryfall_sell_cans = {}
scryfall_buy_cans = {}

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
        scryfall_sell_cans[card] = zscore
    if zscore < -1.96:
        scryfall_buy_cans[card] = zscore

#print the buy and sell candidates according to the Scryfall data
print('Scryfall data:')
print(f'Sell candidates- {scryfall_sell_cans}')
print('\n')
print(f'Buy candidates- {scryfall_buy_cans}')

#begin same process for MTGO Collection prices
file2 = open('MTGOCollectionPrices.json')
data2 = json.load(file2)
file2.close()

mtgo_sell_cans = {}
mtgo_buy_cans = {}

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
        mtgo_sell_cans[card] = zscore
    if zscore < -1.96 and delta.days < 10:
        mtgo_buy_cans[card] = zscore

print('\n')
print('Cardhoarder data:')
print(f'Sell candidates- {mtgo_sell_cans}')
print('\n')
print(f'Buy candidates- {mtgo_buy_cans}')

# set up Tkinter window, frames, labels
window = tk.Tk()
window.rowconfigure([0,1], weight=1)
window.columnconfigure([1], weight=1)

frm_scryfall = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=5)
frm_scryfall.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

lbl_scryfall_title = tk.Label(master=frm_scryfall, text='Scryfall data:', font='bold', fg='steel blue')
lbl_scryfall_title.pack()

lbl_scryfall_sell_cans = tk.Label(master=frm_scryfall, text=f'Sell candidates - {scryfall_sell_cans}', wraplength=1440, justify='left')
lbl_scryfall_sell_cans.pack()

lbl_scryfall_buy_cans = tk.Label(master=frm_scryfall, text=f'Buy candidates - {scryfall_buy_cans}', wraplength=1440, justify='left')
lbl_scryfall_buy_cans.pack()

frm_mtgo = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=5)
frm_mtgo.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

lbl_mtgo_title = tk.Label(master=frm_mtgo, text='MTGO data:', font='bold', fg='steel blue')
lbl_mtgo_title.pack()

lbl_mtgo_sell_cans = tk.Label(master=frm_mtgo, text=f'Sell candidates - {mtgo_sell_cans}', wraplength=1440, justify='left')
lbl_mtgo_sell_cans.pack()

lbl_mtgo_buy_cans = tk.Label(master=frm_mtgo, text=f'Buy candidates - {mtgo_buy_cans}', wraplength=1440, justify='left')
lbl_mtgo_buy_cans.pack()

window.mainloop()