import os
import requests
import pandas as pd

from dotenv import load_dotenv

load_dotenv('.env')

from log import log
from utils import ( epoc_to_datetime )

endpoint = 'data/v2/histoday'
headers = {
    'Authorization': 'Apikey {}'.format(os.getenv('CRYPTO_COMPARE_API_KEY') )
}

# load coin data
coins_df = pd.read_csv('coins.csv')

if not os.path.exists('price_data'):
    os.makedirs('price_data')

for index, row in coins_df.iterrows():
    # create new price data frame
    if row['CirculatingSupply'] == 0 or pd.isna( row['CirculatingSupply'] ):
        log('skipping {}: 0 coins in circulation supply'.format(row['Symbol']), type= 'warning')
        continue

    price_df = pd.DataFrame()

    # retrieve all coin historical price daily data
    payload = {'fsym': row['Symbol'], 'tsym': 'USD', 'allData': 'true' }
    response = requests.get('https://{}/{}'.format(os.getenv('CRYPTO_COMPARE_HOSTNAME'), endpoint), headers = headers, params = payload)
    if response.json().get('Response').lower() == 'error':
        log('Skipping Error: {}'.format(response.json().get('Message') ), type='warning')
        continue

    # convert to dataframe
    has_started = False
    for content in response.json()['Data']['Data']:
        if content['high'] == 0 and content['low'] == 0 and content['close'] == 0 and has_started == False:
            continue
        content['time'] = epoc_to_datetime(content['time']).strftime('%Y-%m-%d')
        price_df = price_df.append(content, ignore_index = True)
        has_started = True

    # export to csv
    price_df.to_csv('./price_data/{}.csv'.format(row['Symbol']), index=False)
