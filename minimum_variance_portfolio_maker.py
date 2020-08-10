import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import quandl
#import scipy.optimize as scoplt.style.use('fivethirtyeight')
np.random.seed(777) 

def price_maker(tickers):
    df_concated = pd.DataFrame()
    for ticker_name in tickers:
        ticker = Ticker(ticker_name)
        df = ticker.history(period='max', interval='1d', start='2016-01-04', end='2017-12-29')
        try:
            df_concated = pd.concat([df_concated, df['close'].rename(str(ticker_name))], axis=1)
        except KeyError:
            print("ticker_name: ", ticker_name)
    return df_concated

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
    max_sharpe_allocation = pd.DataFrame(weights[max_sharpe_idx],index=df.columns,columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i*100,2)for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T
    
    min_vol_idx = np.argmin(results[0])
    sdp_min, rp_min = results[0,min_vol_idx], results[1,min_vol_idx]
    min_vol_allocation = pd.DataFrame(weights[min_vol_idx],index=df.columns,columns=['allocation'])
    min_vol_allocation.allocation = [round(i*100,2)for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T
    
    
    return max_sharpe_allocation, min_vol_allocation

def main():
    df_red = pd.read_csv('C:/Users/antoi/Documents/Programming/portfolio-advisor/dashboard/data/tickers_september_2017_red.csv')
    tickers = df_red['Ticker'].values
    df = price_maker(tickers)
    df.index = pd.to_datetime(df.index)
    df = df.resample("1D").sum()
    df = df[~df.isin([0])].dropna() # getting rid of weekends where stocks = 0
    returns = df.pct_change()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_portfolios = 5000000#25000
    risk_free_rate = 0.0178
    max_sharpe_al, min_vol_al = display_simulated_ef_with_random(mean_returns, cov_matrix, num_portfolios, risk_free_rate, df)
    min_vol_allocation_sorted = min_vol_al.sort_values(axis = 1, by = 'allocation', ascending=False)
    max_sharpe_allocation_sorted = max_sharpe_al.sort_values(axis = 1, by = 'allocation', ascending=False)
    min_vol_allocation_sorted.to_csv("min_vol_allocation.csv")
    max_sharpe_allocation_sorted.to_csv("max_sharpe_allocation.csv")

if __name__ == '__main__':
    main()  