#!/usr/bin/env python3

import json
import statistics as stats
from datetime import datetime
from datetime import date
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# import Cardhoarder_Scraper
# import Scryfall_API

print('\n')

today = datetime.now().date()
# randomdate = date(2020, 1, 5)

#grab Scryfall price data
file1 = open('ScryfallPriceData.json')
scryfall_data = json.load(file1)
file1.close()

#establish dicts for buy candidates and sell candidates
scryfall_sell_cans = {}
scryfall_buy_cans = {}

#pick the number of days to perform analysis on
x = 60

#grab prices for each card and calculate the z score
for card, dates in scryfall_data.items():
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

# create sorted lists
scryfall_sell_cans_sorted = sorted(scryfall_sell_cans, key=lambda k:scryfall_sell_cans[k], reverse=True)
scryfall_buy_cans_sorted = sorted(scryfall_buy_cans, key=lambda k: scryfall_buy_cans[k])

#print the buy and sell candidates according to the Scryfall data
print('Scryfall data:')
print(f'Sell candidates- {scryfall_sell_cans}')
print('\n')
print(f'Buy candidates- {scryfall_buy_cans}')

#begin same process for MTGO Collection prices
file2 = open('MTGOCollectionPrices.json')
mtgo_data = json.load(file2)
file2.close()

mtgo_sell_cans = {}
mtgo_buy_cans = {}

for card, dates in mtgo_data.items():
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
    if zscore > 1.96 and delta.days < 10 and prices[-1] > 0.10:
        mtgo_sell_cans[card] = zscore
    if zscore < -1.96 and delta.days < 10 and prices[-1 > 0.10]:
        mtgo_buy_cans[card] = zscore

# create sorted lists
mtgo_sell_cans_sorted = sorted(mtgo_sell_cans, key=lambda k: mtgo_sell_cans[k], reverse=True)
mtgo_buy_cans_sorted = sorted(mtgo_buy_cans, key=lambda k: mtgo_buy_cans[k])

print('\n')
print('Cardhoarder data:')
print(f'Sell candidates- {mtgo_sell_cans}')
print('\n')
print(f'Buy candidates- {mtgo_buy_cans}')

# set up Tkinter window, frames, labels
window = tk.Tk()
window.title('MTG Card Price Analysis')
window.rowconfigure([0,1], weight=1)
window.columnconfigure([1], weight=1)

frm_scryfall = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=5)
frm_scryfall.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

lbl_scryfall_title = tk.Label(master=frm_scryfall, text='Scryfall data:', font='bold', fg='steel blue')
lbl_scryfall_title.pack()

lbl_scryfall_sell_cans = tk.Label(master=frm_scryfall, text=f'Sell candidates - {scryfall_sell_cans_sorted}', wraplength=1440, justify='left')
lbl_scryfall_sell_cans.pack()

lbl_scryfall_buy_cans = tk.Label(master=frm_scryfall, text=f'Buy candidates - {scryfall_buy_cans_sorted}', wraplength=1440, justify='left')
lbl_scryfall_buy_cans.pack()

frm_mtgo = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=5)
frm_mtgo.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

lbl_mtgo_title = tk.Label(master=frm_mtgo, text='MTGO data:', font='bold', fg='steel blue')
lbl_mtgo_title.pack()

lbl_mtgo_sell_cans = tk.Label(master=frm_mtgo, text=f'Sell candidates - {mtgo_sell_cans_sorted}', wraplength=1440, justify='left')
lbl_mtgo_sell_cans.pack()

lbl_mtgo_buy_cans = tk.Label(master=frm_mtgo, text=f'Buy candidates - {mtgo_buy_cans_sorted}', wraplength=1440, justify='left')
lbl_mtgo_buy_cans.pack()

# create, grab, and sort all cards from scryfall
scryfall_cards = []
for card in scryfall_data.keys():
    scryfall_cards.append(card)
scryfall_cards = sorted(scryfall_cards)

# assign starting variable to dropdown (below)
starting_card = tk.StringVar()
starting_card.set('Select a card to plot')

def card_price_plotter(*args):
    '''Plots the price of a chosen card from the dropdown menu.'''
    # grab selected card from dropdown
    selected_card = starting_card.get()
    # grab data for selected card
    selected_card_data = scryfall_data[selected_card]
    # establish lists and populate them with the card date and prices
    selected_card_dates, selected_card_prices = [], []
    for date, price in selected_card_data.items():
        selected_card_dates.append(date)
        selected_card_prices.append(float(price))

    # change date string to datetime type
    selected_card_dates_datetime = []
    for date in selected_card_dates:
        selected_card_dates_datetime.append(datetime.strptime(date, '%m-%d-%y'))

    # create plot
    fig, ax = plt.subplots(figsize=(20, 10))

    # plot dates, prices
    ax.plot(selected_card_dates_datetime, selected_card_prices, color='blue')
    # set axes and title
    ax.set(xlabel='Date', ylabel='Price (tix)', title=f'Price Data for {selected_card}')
    # format x-axis
    date_format = mdates.DateFormatter('%m-%d')
    ax.xaxis.set_major_formatter(date_format)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    # show plot
    plt.show()

# create dropdown for card price plotter
drop_cards = tk.OptionMenu(window, starting_card, *scryfall_cards, command=card_price_plotter)
drop_cards.grid(row=2, column=1)

window.mainloop()