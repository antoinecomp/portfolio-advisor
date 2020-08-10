from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options



import pandas as pd
import numpy as np

from collections import defaultdict
import json

import time

import requests
from requests.exceptions import ConnectionError

# Define Browser Options
chrome_options = Options()
chrome_options.add_argument("--headless") # Hides the browser window

# Reference the local Chromedriver instance
chrome_path = r"C:\Programs\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

df = pd.read_csv('C:/Users/antoi/Downloads/tickers_september_2017_updated.csv')    

tradable = []
print(len(df['Ticker']))
for ticker in df['Ticker']:
    print("ticker: ", ticker)
    location = "https://www.etoro.com/markets/" + ticker.lower()
    try:
        request = requests.get(location)
        driver.get(location)
        time.sleep(2)
        current_url = driver.current_url
        if current_url == location:
            tradable.append(ticker)
        else:
            print("no page but request= ", request)
    except ConnectionError:
        print('Ticker isn\'t tradable')
    else:
        tradable.append(ticker)