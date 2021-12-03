from datetime import datetime
import os
import requests
import pandas as pd

from dotenv import load_dotenv
load_dotenv('.env')

from log import log
from utils import ( epoc_to_datetime )

endpoint = 'data/social/coin/histo/day'
headers = {
    'Authorization': 'Apikey {}'.format(os.getenv('CRYPTO_COMPARE_API_KEY') )
}

if not os.path.exists('social_data'):
    os.makedirs('social_data')

# load coin data
coins_df = pd.read_csv('coins.csv')
total_coins_found = 0
for index, row in coins_df.iterrows():

    # create new price data frame
    if row['CirculatingSupply'] == 0 or pd.isna( row['CirculatingSupply'] ):
        log('Skipping {}: No coins in circulation supply'.format(row['Symbol']), type= 'warning')
        continue

    # create new social data frame
    social_df = pd.DataFrame()

    # retrieve all coin historical price daily data
    is_done = False
    toTs = None
    while not is_done:
        payload = {'coinId': row['Id'], 'limit': 2000}
        if toTs:
            payload['toTs'] =  toTs

        response = requests.get('https://{}/{}'.format(os.getenv('CRYPTO_COMPARE_HOSTNAME'), endpoint), headers = headers, params = payload)
        if response.json().get('Response').lower() == 'error':
            log('Skipping Error: {}'.format(response.json().get('Message') ), type='warning')
            continue

        # convert to dataframe
        data = response.json().get('Data', [])
        toTs = data[0]['time']

        for content in data:
            content['time'] = epoc_to_datetime(content['time']).strftime('%Y-%m-%d')
            social_df = social_df.append(content, ignore_index = True)

        launch_date = datetime.strptime(row['AssetLaunchDate'], '%Y-%m-%d')

        if epoc_to_datetime(toTs) < launch_date:
            is_done = True

    # export to csv
    social_df.to_csv('./social_data/{}.csv'.format(row['Symbol']), index=False)
    log('Success: {}'.format(row['Symbol']), type='success')
    total_coins_found += 1

log('Total Coins: {} / {}'.format(total_coins_found, len(coins_df)), type='success')
