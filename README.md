The purpose of this project is to scrape together MTG card prices from two sources: Scryfall's API and your personal collection on Cardhoarder.com.
Scryfall_API.py accomplishes this by pulling API URLs from the ScryfallURLs.py file and making calls to the Scryfall API.
Cardhoarder_Scraper.py pulls data from Cardhoarder by controlling a browser via Selenium. 
  The script looks for Cardhoarder login credentials in a Passwords.py file and file paths in a Config.py file. You'll need to make and store these files in the same directory.
The Scryfall data is stored in the ScryfallPriceData.json file while the Cardhoarder data is stored in the MTGOCollectionPrices.json file.
The MTG_Data_Analysis.py file is really the main file to run, it does everything-
    It first runs the Cardhoarder_Scraper.py file, then the Scryfall_API.py file, 
    and then it does basic Z-score analysis on the card prices to develop a list of buy and sell candidates.
  
The data I have collected may not be used for commercial use.
