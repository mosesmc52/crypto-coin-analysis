import pandas as pd
from log import log
import os

total_coins = len(pd.read_csv('coins.csv'))
total_social_data_coins = len(os.listdir('social_data/'))
total_price_data_coins = len(os.listdir('price_data/'))
total_merged_data_coins = len(os.listdir('merge_price_social/'))

log('Total Coins: {}'.format(total_coins), 'info')
log('Total Social Data Coins: {}'.format(total_social_data_coins), 'success')
log('Total Price Data Coins: {}'.format(total_price_data_coins), 'success')
log('Merged Coins: {}'.format(total_merged_data_coins), 'success')

log('Tickers', 'success')
for file in os.listdir('merge_price_social/'):
    print(file.replace('.csv',''))
