#!/usr/bin/env python3
import os
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from Kwargs import *
from Config import *
import time
import json
from datetime import datetime

file1 = open('MTGOCollectionPrices.json')
data = json.load(file1)
file1.close()

today = datetime.today().strftime('%m-%d-%Y')

options = Options()
options.add_argument('--incognito')
options.add_argument('start-maximized')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

options.binary_location = binary_location
browser = webdriver.Chrome(options = options, executable_path= executable_path)

pagenum = 1

browser.execute_script(f"window.open('{chLink}')")
handles = browser.window_handles
browser.switch_to.window(handles[-1])
elem = browser.find_element_by_id('UserEmail')
elem.clear()
elem.send_keys(chUser)
elem = browser.find_element_by_id('UserPassword')
elem.clear()
elem.send_keys(chPw)
browser.find_element_by_xpath('//input[@class="btn btn-lg btn-primary"][@value="Log In"]').click()
assert 'Your Cardhoarder Dashboard' in browser.title
browser.find_element_by_xpath('//a[@href="/card-keeper"]').click()
time.sleep(2)
assert 'Card Keeper Tool' in browser.title
time.sleep(2)
elems = browser.find_elements_by_xpath(
    '//button[@class="btn btn-sm btn-default dropdown-toggle"][@data-toggle="dropdown"]')
time.sleep(0.5)
elems[0].click()
browser.find_element_by_xpath('//*[@id="setting-toggles"]/div[2]/ul/li[4]/a').click()
time.sleep(2)
elems[1].click()
browser.find_element_by_xpath('//*[@id="setting-toggles"]/div[3]/ul/li[3]/a').click()
browser.find_element_by_xpath('//*[@id="active-filters"]/div[2]/a/span').click()
browser.find_element_by_xpath('//*[@id="settings-panel"]/div[1]/div/a[1]').click()

browser.find_element_by_xpath('//*[@id="setting-toggles"]/div[1]/button[3]').click()
prices = []
cards = []
sets = []
foils = []

while pagenum <21:
    time.sleep(3)
    elems = browser.find_elements_by_xpath('//*[@id="cards-table"]/tbody/tr/td/a')
    for element in elems:
        cards.append(element.get_attribute('innerHTML'))

    elems = browser.find_elements_by_xpath('//*[@id="cards-table"]/tbody/tr/td[2]')
    for element in elems:
        sets.append(element.get_attribute('innerHTML'))

    elems = browser.find_elements_by_xpath('//*[@id="cards-table"]/tbody/tr/td[6]')
    for element in elems:
        prices.append(element.get_attribute('innerHTML'))

    elems = browser.find_elements_by_xpath('//*[@id="cards-table"]/tbody/tr')
    for element in elems:
        if 'https://d17uu2v7oycgti.cloudfront.net/site_assets/isfoil.png' in element.get_attribute('innerHTML'):
            foils.append('yes')
        else:
            foils.append('no')

    pagenum += 1
    if pagenum <21:
        browser.find_element_by_xpath('//*[@id="settings-panel"]/div[2]/ul/li[7]/a').click()
    else:
        pass

bigdict = {}
bigdict['cards'] = cards
bigdict['sets'] = sets
bigdict['foils'] = foils
bigdict['prices'] = prices

for i in range(0, len(cards)):
    if bigdict['foils'][i] == 'yes':
        name = bigdict['cards'][i]
        set = bigdict['sets'][i]
        price = bigdict['prices'][i]
        cardname = f'{name} - {set} (foil)'
    else:
        name = bigdict['cards'][i]
        set = bigdict['sets'][i]
        price = bigdict['prices'][i]
        cardname = f'{name} - {set}'
    try:
        data[cardname][today] = price
    except:
        data[cardname] = {}
        data[cardname][today] = price

file1 = open('MTGOCollectionPrices.json', 'w')
json.dump(data, file1)
file1.close()

print('Success')