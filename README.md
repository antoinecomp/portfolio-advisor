# Portfolio advisor

Aggregator of companies meeting Benjamin Graham's rules for defensive investor profile. 
That is to say: 

 - Sales above $700m.
 - Conservatively financed: assets at least twice as large as liabilities.
 - Uninterrupted dividends for 20 years
 - No earnings deficit for 10 years
 - Earnings growth of at least 2.9% per year on average for the last 10 years.

Nice to have, but as a matter of comparison with other companies:
 - Cheap assets: Market cap < (Assets - Liabilities) * 1.5
 - Cheap earnings: price/earnings < 15
 
 ## To run
`python run.py`
 
 ## To do
  - Get all the Yahoo tickers
  - Display all tickers that respect Graham rules in a comprehensive way, 
  so when we click on them we get what we have atm in the stock view
  - Find Sales, average of earnings growth over 10 years, earnings
  - Finish current ratio