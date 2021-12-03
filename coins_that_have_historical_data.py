from datetime import datetime
import csv
from os import listdir
from os.path import isfile, join
import pandas as pd

MIN_YEARS = 2
DAYS_IN_YEAR = 365
price_tickers = [f.replace('.csv','').lower() for f in listdir('./price_data') if isfile(join('./price_data', f))]
coins_df = pd.read_csv('coins.csv')

tickers = []
for index, row in coins_df.iterrows():
    if row.Symbol.lower() in price_tickers:
        years_since_launch = round((datetime.now() - datetime.strptime(row.AssetLaunchDate,'%Y-%m-%d')).days /DAYS_IN_YEAR, 2)

        if years_since_launch > MIN_YEARS:
            tickers.append({
                'symbol': row.Symbol.lower(),
                'url': row.AssetWebsiteUrl,
                'launch date': row.AssetLaunchDate,
                'years since launch': years_since_launch
            })

csv_columns = ['symbol','url','launch date', 'years since launch']
with open('./selected_coins.csv', 'w') as csvfile:
   writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
   writer.writeheader()
   for data in tickers:
       writer.writerow(data)
