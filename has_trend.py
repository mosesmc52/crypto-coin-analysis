from datetime import datetime, timedelta
import os
import requests
import pandas as pd
from log import log
from utils import (momentum_quality, momentum_score , volatility, str2bool)

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from SES import ( AmazonSES )

LOOKBACK_PERIOD_MONTHS = 12
QUALITY_SUCCESS_RATIO = 2/3

DAYS_IN_MONTH = 30
MIN_INF_DISCR = 0.0
MIN_MOMENTUM_SCORE = 500.0
coins_df = pd.read_csv('selected_coins.csv')

lookback_end = datetime.now() - timedelta( days = DAYS_IN_MONTH)
#lookback_end = datetime.now()

past_date = datetime.now() - timedelta( days = LOOKBACK_PERIOD_MONTHS * DAYS_IN_MONTH)
has_trend = []
runners_up = []
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
    inf_discr, positive_sum, is_quality = momentum_quality(df['close'][past_date.strftime('%Y-%m-%d'): lookback_end.strftime('%Y-%m-%d')], min_inf_discr = MIN_INF_DISCR, lookback_months = LOOKBACK_PERIOD_MONTHS, quality_success_ratio = QUALITY_SUCCESS_RATIO)

    if not is_quality:
        log(' > Quality failed', 'error')


    # calculate momentum score
    score = momentum_score(df['close'][past_date.strftime('%Y-%m-%d'): lookback_end.strftime('%Y-%m-%d')]).mean()
    if score <= float(MIN_MOMENTUM_SCORE):
        log(' > Score {0} less than minimum'.format(score))
    else:
        print(' > Momentum Score: {}'.format(round(score, 3)))

    print(' > Volatility: {}'.format(round(volatility(df['close'][past_date.strftime('%Y-%m-%d'): lookback_end.strftime('%Y-%m-%d')]), 3)))

    if is_quality:
        log(' > Pass', 'success')
        has_trend.append({
            'symbol': symbol,
            'score': score,
            'positive_sum': positive_sum,
            'volatility': volatility(df['close'][past_date.strftime('%Y-%m-%d'): lookback_end.strftime('%Y-%m-%d')])
        })
    elif score > MIN_MOMENTUM_SCORE:
        runners_up.append({
            'symbol': symbol,
            'score': score,
            'positive_sum': positive_sum,
            'volatility': volatility(df['close'][past_date.strftime('%Y-%m-%d'): lookback_end.strftime('%Y-%m-%d')])
        })

message_body_html = '<b>Coins Pass (> {} Months positive return)</b><br>'.format(LOOKBACK_PERIOD_MONTHS)
print('\n')
log('Coins Pass (> {} Months positive return)'.format(LOOKBACK_PERIOD_MONTHS), 'success')
for item in has_trend:
    # calculate volatility
    log('Symbol: {}, Positive Months: {}, Momentum Score: {}, Volatility: {}'.format(item['symbol'], round(item['positive_sum'], 3), round(item['score'], 3), round(item['volatility'], 3)), 'info')
    message_body_html +=  'Symbol: {}, Positive Months: {}, Momentum Score: {}, Volatility: {}<br>'.format(item['symbol'], round(item['positive_sum'], 3), round(item['score'], 3), round(item['volatility'], 3))

print('\n')
log('Coins Meet mimimum Momentum Score (> {})'.format(MIN_MOMENTUM_SCORE), 'success')
message_body_html += '<br><b>Coins Meet mimimum Momentum Score (> {})</b><br>'.format(MIN_MOMENTUM_SCORE)
for item in runners_up:
    # calculate volatility
    log('Symbol: {}, Positive Months: {}, Momentum Score: {}, Volatility: {}'.format(item['symbol'], round(item['positive_sum'], 3), round(item['score'], 3), round(item['volatility'], 3)), 'info')
    message_body_html +=  'Symbol: {}, Positive Months: {}, Momentum Score: {}, Volatility: {}<br>'.format(item['symbol'], round(item['positive_sum'], 3), round(item['score'], 3), round(item['volatility'], 3))

if str2bool(os.getenv('EMAIL_POSITIONS', False)):
    TO_ADDRESSES = os.getenv('TO_ADDRESSES', '').split(',')
    FROM_ADDRESS = os.getenv('FROM_ADDRESS', '')
    ses = AmazonSES(region = os.environ.get('AWS_SES_REGION_NAME'),
                    access_key = os.environ.get('AWS_SES_ACCESS_KEY_ID'),
                    secret_key= os.environ.get('AWS_SES_SECRET_ACCESS_KEY'),
                    from_address = os.environ.get('FROM_ADDRESS')
                    )

    subject = "Your Monthly Crypto Momentum Report"

    for to_address in TO_ADDRESSES:
        ses.send_html_email( to_address = to_address, subject = subject, content = message_body_html)
