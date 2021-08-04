#!/usr/bin/env python3

import json
import statistics as stats
from datetime import datetime
from datetime import date
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import askyesno
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtickers
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sys import exit


def on_exit(window):
    """Asks for confirmation to exit"""
    if askyesno('Exit confirmation', 'Are you sure you want to quit?'):
        window.destroy()
        exit()


# create start window
start_window = tk.Tk()
start_window.title('Welcome')
start_window.config(bg='gray37')


def yes_press():
    """Runs the Cardhoarder and Scryfall scripts if yes button is pushed."""
    start_window.destroy()
    start_window.quit()
    try:
        import Cardhoarder_Scraper
    except Exception as error:
        print('Unable to complete scraping of CH data:')
        print(error)
    try:
        import Scryfall_API
    except Exception as error:
        print('Unable to complete collection of data from Scryfall:')
        print(error)


def no_press():
    """Destroys and quits start window if no button is pushed."""
    start_window.destroy()
    start_window.quit()


# create label and yes / no buttons
txt_question = tk.Label(text='Do you want to scrape data?', bg='gray37', fg='white')
txt_question.pack()

frm_yes_no_buttons = tk.Frame(master=start_window)
frm_yes_no_buttons.pack()

btn_yes = tk.Button(master=frm_yes_no_buttons, text='Yes', width=20, height=5, command=yes_press, bg='gray60', fg='white')
btn_yes.pack(side=tk.LEFT)

btn_no = tk.Button(master=frm_yes_no_buttons, text='No', width=20, height=5, command=no_press, bg='gray60', fg='white')
btn_no.pack(side=tk.LEFT)

# open start window
start_window.protocol('WM_DELETE_WINDOW', lambda: on_exit(start_window))
start_window.mainloop()

today = datetime.now().date()

# grab Scryfall price data
file1 = open('ScryfallPriceData.json')
scryfall_data = json.load(file1)
file1.close()

# establish dicts for buy candidates and sell candidates
scryfall_sell_cans = {}
scryfall_buy_cans = {}

# pick the number of days to perform analysis on
days = 60

# grab prices for each card and calculate the z score
for card, dates in scryfall_data.items():
    price_list = [price for price in dates.values()]
    prices = [float(price) for price in price_list]
    prices = prices[-days:]
    if len(prices) >= days:
        avg = stats.mean(prices)
        std = stats.stdev(prices)
        try:
            zscore = (prices[-1]-avg)/std
        except ZeroDivisionError:
            zscore = 0
        # if the zscore is above/below two std devs, add to the proper candidate list
        if zscore > 1.96:
            scryfall_sell_cans[card] = zscore
        if zscore < -1.96:
            scryfall_buy_cans[card] = zscore

# begin same process for MTGO Collection prices
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
    prices = prices[-days:]
    avg = stats.mean(prices)
    if len(prices) > 1:
        std = stats.stdev(prices)
    else:
        pass
    try:
        zscore = (prices[-1] - avg) / std
    except ZeroDivisionError:
        zscore = 0
    if zscore > 1.96 and delta.days < 5 and prices[-1] > 0.10:
        mtgo_sell_cans[card] = zscore
    if zscore < -1.96 and delta.days < 5 and prices[-1 > 0.10]:
        mtgo_buy_cans[card] = zscore

# sort the buy and sell candidates by lowest and highest z-scores
scryfall_sell_cans_sorted = sorted(scryfall_sell_cans, key=lambda k:scryfall_sell_cans[k], reverse=True)
scryfall_buy_cans_sorted = sorted(scryfall_buy_cans, key=lambda k: scryfall_buy_cans[k])
mtgo_sell_cans_sorted = sorted(mtgo_sell_cans, key=lambda k: mtgo_sell_cans[k], reverse=True)
mtgo_buy_cans_sorted = sorted(mtgo_buy_cans, key=lambda k: mtgo_buy_cans[k])

# set up Tkinter window, frames, labels
window = tk.Tk()
window.title('MTG Card Price Analysis')
window.config(bg='white')
window.rowconfigure([0, 1], weight=1)
window.columnconfigure([1], weight=1)

# establish background and text colors
bg_color = 'snow'
fg_text = 'blue4'

frm_scryfall = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=5, bg=bg_color)
frm_scryfall.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

lbl_scryfall_title = tk.Label(master=frm_scryfall, text='Scryfall data:', font='bold', fg='steel blue', bg=bg_color)
lbl_scryfall_title.pack()

lbl_scryfall_sell_cans = tk.Label(master=frm_scryfall, text=f'Sell candidates - {scryfall_sell_cans_sorted}', wraplength=1440, justify='left',
                                  bg=bg_color, fg=fg_text)
lbl_scryfall_sell_cans.pack()

lbl_scryfall_buy_cans = tk.Label(master=frm_scryfall, text=f'Buy candidates - {scryfall_buy_cans_sorted}', wraplength=1440, justify='left',
                                 bg=bg_color, fg=fg_text)
lbl_scryfall_buy_cans.pack()

frm_mtgo = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=5, bg=bg_color)
frm_mtgo.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

lbl_mtgo_title = tk.Label(master=frm_mtgo, text='MTGO data:', font='bold', fg='steel blue', bg=bg_color)
lbl_mtgo_title.pack()

lbl_mtgo_sell_cans = tk.Label(master=frm_mtgo, text=f'Sell candidates - {mtgo_sell_cans_sorted}', wraplength=1440, justify='left', bg=bg_color,
                              fg=fg_text)
lbl_mtgo_sell_cans.pack()

lbl_mtgo_buy_cans = tk.Label(master=frm_mtgo, text=f'Buy candidates - {mtgo_buy_cans_sorted}', wraplength=1440, justify='left', bg=bg_color,
                             fg=fg_text)
lbl_mtgo_buy_cans.pack()

# create, grab, and sort all cards from Scryfall
scryfall_cards = [card for card in scryfall_data.keys()]
scryfall_cards = sorted(scryfall_cards)

# assign starting variable to dropdown (below)
starting_card = tk.StringVar()
starting_card.set('Select a card to plot')

# establish graph variables to be used in plotter function
canvas = None
fig, ax = plt.subplots(figsize=(20, 8))
colors = ['blue', 'red', 'green', 'purple', 'darkorange', 'saddlebrown', 'slategrey', 'deepskyblue', 'gold']
color_count = 0
legend_tuple = ()


def card_price_plotter(*args):
    """Plots the price of a chosen card from the dropdown menu."""
    global canvas, fig, ax, color_count, legend_tuple
    # clear the canvas if it is not empty
    if canvas != None:
        canvas._tkcanvas.destroy()

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

    # plot dates, prices
    ax.plot(selected_card_dates_datetime, selected_card_prices, color=colors[color_count])

    # add card to legend_tuple
    legend_tuple += (selected_card,)

    # set axes and title
    ax.set(xlabel='Date', ylabel='Price (tix)')
    # format x-axis
    date_format = mdates.DateFormatter('%m-%d')
    ax.xaxis.set_major_formatter(date_format)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    # format y-axis
    ax.set_yscale('log')
    ax.yaxis.set_major_formatter(mtickers.ScalarFormatter())
    # format legend
    ax.legend(labels=legend_tuple)

    # show plot
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.get_tk_widget().grid(row=3, column=1)

    # increment color_count
    if color_count == (len(colors) - 1):
        color_count = 0
    else:
        color_count += 1


def canvas_reset():
    """Resets the canvas and other other variables"""
    global canvas, fig, ax, color_count, legend_tuple, starting_card
    try:
        canvas._tkcanvas.destroy()
        fig, ax = plt.subplots(figsize=(20, 8))
        color_count = 0
        legend_tuple = ()
        starting_card.set('Select a card to plot')
    except:
        pass


# create frame for card dropdown and clear button
frm_buttons = tk.Frame(master=window, borderwidth=5, bg=bg_color)
frm_buttons.grid(row=2, column=1)

# create and format dropdown for card price plotter
combo_style = ttk.Style()
combo_style.theme_create('combo_style', settings={'TCombobox': {'configure': {'selectbackground': bg_color, 'selectforeground': fg_text, 'fieldbackground': bg_color,'fieldforeground': fg_text, 'background': bg_color, 'foreground': fg_text}}})
combo_style.theme_use('combo_style')
combo_cards = ttk.Combobox(frm_buttons, textvariable=starting_card, values=scryfall_cards, width=54)
combo_cards.bind("<<ComboboxSelected>>", card_price_plotter)
frm_buttons.option_add("*TCombobox*Listbox*Background", bg_color)
frm_buttons.option_add("*TCombobox*Listbox*Foreground", fg_text)
combo_cards.pack(side=tk.LEFT)

# create clear graph button
btn_clear = tk.Button(frm_buttons, text='Clear graph', bg=bg_color, fg=fg_text, command=canvas_reset)
btn_clear.pack(side=tk.LEFT)

# end if window closed
window.protocol('WM_DELETE_WINDOW', lambda: on_exit(window))

window.mainloop()