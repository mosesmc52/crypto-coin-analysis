import os
import requests
import pandas as pd

from dotenv import load_dotenv

load_dotenv('.env')
from log import log

if not os.path.exists('merge_price_social'):
    os.makedirs('merge_price_social')

coins_df = pd.read_csv('selected_coins.csv')

for index, row in coins_df.iterrows():
    price_df = pd.read_csv('./price_data/{}.csv'.format(row.symbol.upper()))
    social_df = pd.read_csv('./social_data/{}.csv'.format(row.symbol.upper()))
    merge_df = pd.merge(price_df, social_df, on=["time"])
    merge_df.to_csv('./merge_price_social/{}.csv'.format(row['symbol'].upper()), index=False)
    log('{} merged'.format(row['symbol'].upper()), 'success')
