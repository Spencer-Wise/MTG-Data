from datetime import datetime
import time
import json
import requests
from ScryfallURLs import *

#grab all URLs
urls = URLS

#print today's date
today = datetime.now().date().strftime('%m-%d-%y')
print(today)

#open json and grab data
file1 = open('ScryfallPriceData.json')
data = json.load(file1)
file1.close()

#establish function to grab card prices from Scryfall and format them
def CardPrice(url):
    res = requests.get(url)
    info = json.loads(res.text)
    card_name = info['name']
    set = info['set'].upper()
    full_name = card_name+' '+set
    price = info['prices']['tix']
    return full_name, price

#test one card to see if data has changed since the last update
prices_MB = data["Mishra's Bauble CSP"]
for v in prices_MB.values():
    prices_list = []
    prices_list.append(v)
recent_MB = prices_list[-1]
current_MB = CardPrice('https://api.scryfall.com/cards/8a720448-017f-4f4a-9501-678245eaed17')[1]

#establish a quit variable
quit = 0

#if the first test came back as price unchanged, check two other cards. If those prices haven't changed, end program
if current_MB == recent_MB:
    print(recent_MB, 'vs', current_MB)
    print('MB\'s price hasn\'t changed. Looking at LOTV.')
    prices_LOTV = data['Liliana of the Veil ISD']
    prices_list = []
    for v in prices_LOTV.values():
        prices_list.append(v)
    last_LOTV = prices_list[-1]
    recent_LOTV = CardPrice('https://api.scryfall.com/cards/ac506c17-adc8-49c6-9d8d-43db7cb1ec9d')[1]
    print(last_LOTV, 'vs', recent_LOTV)
    if recent_LOTV == last_LOTV:
        print('LOTV\'s price has\'nt changed. Looking at Urza.')
        prices_URZA = data['Urza, Lord High Artificer MH1']
        prices_list = []
        for v in prices_URZA.values():
            prices_list.append(v)
        last_URZA = prices_list[-1]
        recent_URZA = CardPrice('https://api.scryfall.com/cards/9e7fb3c0-5159-4d1f-8490-ce4c9a60f567')[1]
        print(last_URZA, 'vs', recent_URZA)
        if last_URZA == recent_URZA:
            print('Urza\'s price hasn\'t changed either. It appears prices have not changed since the last update.')
            quit = 1

if quit == 0:
    #print starting process to show card prices changed
    print('Starting process')

    #run through each URL and grab the card price
    for url in urls:
        info = CardPrice(url)
        full_name = info[0]
        price = info[1]
        if price is None:
            print(f'{full_name} has no price.')
        else:
            #try to add new data to previous data in json, else create a new dict key (for new cards)
            try:
                data[full_name][today] = price
            except:
                data[full_name] = {}
                data[full_name][today] = price
            time.sleep(0.15)

    #dump the data back into the json
    file1 = open('ScryfallPriceData.json', 'w')
    json.dump(data, file1)
    file1.close()

    print('Success!')

