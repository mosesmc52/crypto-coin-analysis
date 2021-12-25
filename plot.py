import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from log import log
import seaborn as sns

#START_TIME = '2018-01-01'
COMPARE_PARAMS = ['points']

coins_df = pd.read_csv('selected_coins.csv')
for index, row in coins_df.iterrows():
    symbol = row.symbol.upper()

    # load data
    df = pd.read_csv('./merge_price_social/{}.csv'.format(symbol))

    # cover time string data to datatime
    df['time'] = pd.to_datetime(df['time'])

    # set time as timeseries index
    df = df.set_index('time')

    # start at start time
    #df = df[START_TIME:]

    # convert daily data to monthly
    df= df.resample('1M').mean()

    # calculate percent change
    #df.pct_change(periods = 1)

    # create directory if it doesn't exist
    if not os.path.exists('plots'):
        os.makedirs('plots')

    # price plot and save data
    df.plot(title=symbol, y=['close'] + COMPARE_PARAMS, logy = True)
    plt.savefig("./plots/{}_time.png".format(symbol.lower()))

    # correlation plot
    sns.heatmap(df[['close'] + COMPARE_PARAMS].corr(), annot = True, fmt='.2g',cmap= 'coolwarm').figure.savefig("./plots/{}_corr.png".format(symbol.lower()))

    log('{} Correlation'.format(symbol), 'success')
    print(df[['close'] + COMPARE_PARAMS].corr())
