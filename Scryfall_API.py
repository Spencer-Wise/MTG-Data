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
    cardname = info['name']
    set = info['set'].upper()
    fullname = cardname+' '+set
    price = info['prices']['tix']
    return fullname, price

#test one card to see if data has changed since the last update
MBprices = data["Mishra's Bauble CSP"]
for v in MBprices.values():
    priceslist = []
    priceslist.append(v)
MBlast = priceslist[-1]
currentMB = CardPrice('https://api.scryfall.com/cards/8a720448-017f-4f4a-9501-678245eaed17')[1]

#if the first test came back as price unchanged, check two other cards. If those prices haven't changed, end program
if currentMB == MBlast:
    print(MBlast, currentMB)
    print('MB\'s price hasn\'t changed. Looking at LOTV.')
    LOTVprices = data['Liliana of the Veil ISD']
    priceslist = []
    for v in LOTVprices.values():
        priceslist.append(v)
    LOTVlast = priceslist[-1]
    currentLOTV = CardPrice('https://api.scryfall.com/cards/ac506c17-adc8-49c6-9d8d-43db7cb1ec9d')[1]
    print(LOTVlast, currentLOTV)
    if currentLOTV == LOTVlast:
        print('LOTV\'s price has\'nt changed. Looking at Urza.')
        Urzaprices = data['Urza, Lord High Artificer MH1']
        priceslist = []
        for v in Urzaprices.values():
            priceslist.append(v)
        Urzalast = priceslist[-1]
        currentUrza = CardPrice('https://api.scryfall.com/cards/9e7fb3c0-5159-4d1f-8490-ce4c9a60f567')[1]
        print(Urzalast, currentUrza)
        if Urzalast == currentUrza:
            print('Urza\'s price hasn\'t changed either. It appears prices have not changed since the last update.')
            quit()

#print starting process to show card prices changed
print('Starting process')

#run through each URL and grab the card price
for url in urls:
    info = CardPrice(url)
    fullname = info[0]
    price = info[1]
    if price is None:
        print(f'{fullname} has no price.')
    else:
        #try to add new data to previous data in json, else create a new dict key (for new cards)
        try:
            data[fullname][today] = price
        except:
            data[fullname] = {}
            data[fullname][today] = price
        time.sleep(0.15)

#dump the data back into the json
file1 = open('ScryfallPriceData.json', 'w')
json.dump(data, file1)
file1.close()

print('Success!')

