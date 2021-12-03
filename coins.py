import os
import requests
import pandas as pd

from dotenv import load_dotenv
load_dotenv('.env')

# retrieve all crypto coins
endpoint = 'data/all/coinlist'
headers = {
    'Authorization': 'Apikey {}'.format(os.getenv('CRYPTO_COMPARE_API_KEY') )
}
response = requests.get('https://{}/{}'.format(os.getenv('CRYPTO_COMPARE_HOSTNAME'), endpoint), headers = headers)
if response.json().get('Response').lower() == 'error':
    print('Error: {}'.format(response.json().get('Message') ))
    quit()

# insert returned data into pandas dataframe
coins_df = pd.DataFrame()
data = response.json().get('Data', {})
for symbol, content in data.items():
    coins_df = coins_df.append(content, ignore_index = True)

# export to csv
coins_df.to_csv('coins.csv', index=False)
