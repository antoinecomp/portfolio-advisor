from collections import defaultdict
import json

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

from selenium.common.exceptions import NoSuchElementException


import pandas as pd
import numpy as np

from collections import defaultdict
import json

import time

import requests
from requests.exceptions import ConnectionError

driver = webdriver.Chrome()

# df = pd.read_csv('C:/Users/antoi/Downloads/tickers_september_2017_updated.csv')
df = pd.read_csv('data/tickers_september_2017_updated.csv')

df = df[df['earnings'].notna()]
df = df[df['earnings']!="-"]
df["earnings"] = df["earnings"].str.replace(',', '')
df["earnings"] = pd.to_numeric(df["earnings"], downcast="float")
df = df.loc[df['dividends']==True]
# df = df.loc[df['ratio']>2] # issue to solve
df = df.loc[df['earnings'] > 200000]

def price_maker(tickers):
    df_concated = pd.DataFrame()
    for ticker_name in tickers:
        ticker = Ticker(ticker_name)
        df = ticker.history(period='max', interval='1d', start='2016-01-04', end='2020-05-08')
        try:
            df_concated = pd.concat([df_concated, df['close'].rename(str(ticker_name))], axis=1)
        except KeyError:
            print("ticker_name: ", ticker_name)
    return df_concated

tradable = []
for ticker in df_red['Ticker']:
    location = "https://www.etoro.com/markets/" + ticker.lower()
    driver.get(location)
    time.sleep(2)
    current_url = driver.current_url
    if current_url == location:
        tradable.append(ticker)
        
df = price_maker(tradable)
df.index = pd.to_datetime(df.index)
df = df.resample("1D").sum()
df = df[~df.isin([0])].dropna() # getting rid of weekends where stocks = 0

def portfolio_annualised_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns*weights ) *252
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    return std, returns
  
def random_portfolios(num_portfolios, mean_returns, cov_matrix, risk_free_rate, df):
    results = np.zeros((3,num_portfolios))
    weights_record = []
    for i in range(num_portfolios):
        weights = np.random.random(len(df.columns))
        weights /= np.sum(weights)
        weights_record.append(weights)
        portfolio_std_dev, portfolio_return = portfolio_annualised_performance(weights, mean_returns, cov_matrix)
        results[0,i] = portfolio_std_dev
        results[1,i] = portfolio_return
        results[2,i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
    return results, weights_record

def display_simulated_ef_with_random(mean_returns, cov_matrix, num_portfolios, risk_free_rate, df):
    results, weights = random_portfolios(num_portfolios,mean_returns, cov_matrix, risk_free_rate, df)
    
    max_sharpe_idx = np.argmax(results[2])
    sdp, rp = results[0,max_sharpe_idx], results[1,max_sharpe_idx]
    print("results[0,max_sharpe_idx], results[1,max_sharpe_idx]: ", results[0,max_sharpe_idx], results[1,max_sharpe_idx])
    max_sharpe_allocation = pd.DataFrame(weights[max_sharpe_idx],index=df.columns,columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i*100,2)for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T
    
    min_vol_idx = np.argmin(results[0])
    sdp_min, rp_min = results[0,min_vol_idx], results[1,min_vol_idx]
    min_vol_allocation = pd.DataFrame(weights[min_vol_idx],index=df.columns,columns=['allocation'])
    min_vol_allocation.allocation = [round(i*100,2)for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T
    
    print("-"*80)
    print("Maximum Sharpe Ratio Portfolio Allocation\n")
    print("Annualised Return:", round(rp,2))
    print("Annualised Volatility:", round(sdp,2))
    print("\n")
    print(max_sharpe_allocation)
    print("-"*80)
    print("Minimum Volatility Portfolio Allocation\n")
    print("Annualised Return:", round(rp_min,2))
    print("Annualised Volatility:", round(sdp_min,2))
    print("\n")
    print(min_vol_allocation)
    
    return max_sharpe_allocation, min_vol_allocation

returns = df.pct_change()
mean_returns = returns.mean()
cov_matrix = returns.cov()
num_portfolios = 1500000
risk_free_rate = 0.0178

min_vol_al, max_sharpe_al = display_simulated_ef_with_random(mean_returns, cov_matrix, num_portfolios, risk_free_rate, df)

max_sharpe_al.to_csv("results.csv")