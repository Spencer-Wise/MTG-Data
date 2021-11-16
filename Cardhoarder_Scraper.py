#!/usr/bin/env python3
import os
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from Config import *
import time
import json
from datetime import datetime

# grab current data from the json file
file1 = open('MTGOCollectionPrices.json')
data = json.load(file1)
file1.close()

# get today's date
today = datetime.today().strftime('%m-%d-%Y')

# set up browser through Selenium
options = Options()
options.add_argument('--incognito')
options.add_argument('start-maximized')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

options.binary_location = binary_location
browser = webdriver.Chrome(options = options, executable_path= executable_path)

# set variable to keep track of pages
page_num = 1

# start browser, navigate to Cardhoarder, log in, select/deselect filters
browser.execute_script(f"window.open('{ch_link}')")
handles = browser.window_handles
browser.switch_to.window(handles[-1])
elem = browser.find_element_by_id('UserEmail')
elem.clear()
elem.send_keys(ch_user)
elem = browser.find_element_by_id('UserPassword')
elem.clear()
elem.send_keys(ch_pw)
browser.find_element_by_xpath('//input[@class="btn btn-lg btn-primary"][@value="Log In"]').click()
assert 'Your Cardhoarder Dashboard' in browser.title
browser.find_element_by_xpath('//a[@href="/card-keeper"]').click()
time.sleep(3)
elems = browser.find_elements_by_xpath(
    '//button[@class="btn btn-sm btn-default dropdown-toggle"][@data-toggle="dropdown"]')
time.sleep(1)
elems[0].click()
browser.find_element_by_xpath('//*[@id="setting-toggles"]/div[2]/ul/li[4]/a').click()
time.sleep(3)
elems[1].click()
browser.find_element_by_xpath('//*[@id="setting-toggles"]/div[3]/ul/li[3]/a').click()
browser.find_element_by_xpath('//*[@id="active-filters"]/div[2]/a/span').click()
browser.find_element_by_xpath('//*[@id="settings-panel"]/div[1]/div/a[1]').click()

browser.find_element_by_xpath('//*[@id="setting-toggles"]/div[1]/button[3]').click()

# establish lists
prices = []
cards = []
sets = []
foils = []

# run through each page and grab the price data
while page_num <21:
    time.sleep(5)
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

    # unless on the last page, navigate to the next page and start the process over
    page_num += 1
    if page_num <21:
        browser.find_element_by_xpath('//*[@id="settings-panel"]/div[2]/ul/li[7]/a').click()
    else:
        pass

# establish dictionary
pulled_card_data = {}
pulled_card_data['cards'] = cards
pulled_card_data['sets'] = sets
pulled_card_data['foils'] = foils
pulled_card_data['prices'] = prices

# format the new data and add it to the previous data from json
for i in range(0, len(cards)):
    if pulled_card_data['foils'][i] == 'yes':
        name = pulled_card_data['cards'][i]
        set = pulled_card_data['sets'][i]
        price = pulled_card_data['prices'][i]
        card_name = f'{name} - {set} (foil)'
    else:
        name = pulled_card_data['cards'][i]
        set = pulled_card_data['sets'][i]
        price = pulled_card_data['prices'][i]
        card_name = f'{name} - {set}'
    try:
        data[card_name][today] = price
    except:
        data[card_name] = {}
        data[card_name][today] = price

# dump the new data back to the json
file1 = open('MTGOCollectionPrices.json', 'w')
json.dump(data, file1)
file1.close()

browser.quit()

print('Success')