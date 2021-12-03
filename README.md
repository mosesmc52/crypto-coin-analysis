## Conduct analysis on Crypto data

### Data Historical Data CryptoCompare.com
https://min-api.cryptocompare.com/

### Setup
`pipenv install`<br>
`pipenv shell`

Required Environmental Variables<br>
CRYPTO_COMPARE_API_KEY<br>
CRYPTO_COMPARE_HOSTNAME<br>

Files and steps fo execution:<br>
1) coins.py<br>
Downloads all of the existing cryptocoins<br>
2) historical_price_data.py<br>
Downloads historical price data<br>
3) historical_social_data.py<br>
Downloads historical social data<br>
4) coins_that_have_historical_data.py<br>
Filters out coins that have both historical price and social data<br>
5) merge_price_social_data.py<br>
Merges historical price and social data<br>

6) plot.py<br>
Plots coin data for analysis. This file produces two plots a correlation and  time series plot<br>

8) has_trend.py<br>
Detects trends within price data<br>

stats.py<br>
Prints out stats on coin<br>
