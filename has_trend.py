from datetime import datetime, timedelta
import os
import requests
import pandas as pd
from log import log
from utils import (momentum_quality, momentum_score , volatility)

LOOKBACK_PERIOD_MONTHS = 12
QUALITY_SUCCESS_RATIO = 2/3

DAYS_IN_MONTH = 30
MIN_INF_DISCR = 0.0
MIN_MOMENTUM_SCORE = 0.0
coins_df = pd.read_csv('selected_coins.csv')

lookback_end = datetime.now() - timedelta( days = DAYS_IN_MONTH)
#lookback_end = datetime.now()

past_date = datetime.now() - timedelta( days = LOOKBACK_PERIOD_MONTHS * DAYS_IN_MONTH)
has_trend = []
for index, row in coins_df.iterrows():
    symbol = row.symbol.upper()
    log(symbol)
    # load data
    df = pd.read_csv('./merge_price_social/{}.csv'.format(symbol))

    # cover time string data to datatime
    df['time'] = pd.to_datetime(df['time'])

    # set time as timeseries index
    df = df.set_index('time')

    # if traded > 100 day MA
    #if df['close'].tail(1).iloc[0] <= df[len(df['close']) - 100:].mean()['close']:
    #    log('Trading below 100 day moving average, skipping', 'warning')
    #    continue

    # if moved > 15% in the past 90 days remove
    #returns = df['close'][len(df['close']) - 90:].pct_change()
    #if len(returns[ (returns <= -.15) | (returns > .15)]):
    #    log('Moved greater than 15% in the past 90 days, skipping', 'warning')
    #    continue

    # calculate inf_discr score
    inf_discr, is_quality = momentum_quality(df['close'][past_date.strftime('%Y-%m-%d'): lookback_end.strftime('%Y-%m-%d')], min_inf_discr = MIN_INF_DISCR, lookback_months = LOOKBACK_PERIOD_MONTHS, quality_success_ratio = QUALITY_SUCCESS_RATIO)
    if not is_quality:
        log(' > Quality failed', 'error')
        continue

    # calculate momentum score
    score = momentum_score(df['close'][past_date.strftime('%Y-%m-%d'): lookback_end.strftime('%Y-%m-%d')]).mean()
    if score <= float(MIN_MOMENTUM_SCORE):
        log(' > Score {0} less than minimum'.format(score))
        continue


    log(' > Pass', 'success')
    has_trend.append({
        'symbol': symbol,
        'score': score,
        'inf_discr': inf_discr,
        'volatility': volatility(df['close'][past_date.strftime('%Y-%m-%d'): lookback_end.strftime('%Y-%m-%d')])
    })

print('\n')
log('Coins Pass ({} Month trend)'.format(LOOKBACK_PERIOD_MONTHS), 'success')
for item in has_trend:
    # calculate volatility
    log('Symbol: {}, Inf Discr: {}, Momentum Score: {}, Volatility: {}'.format(item['symbol'], round(item['inf_discr'], 3), round(item['score'], 3), round(item['volatility'], 3)), 'info')

print('\n')
log('Note(s):', 'warning')
log('Lower the Inf Discr the better. It has a minimum of -1', 'info')
