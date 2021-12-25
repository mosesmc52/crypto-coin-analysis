from datetime import datetime
from scipy import stats
import numpy as np
import pandas as pd

def str2bool(value):
    valid = {'true': True, 't': True, '1': True, 'on': True,
             'false': False, 'f': False, '0': False,
             }

    if isinstance(value, bool):
        return value

    lower_value = value.lower()
    if lower_value in valid:
        return valid[lower_value]
    else:
        raise ValueError('invalid literal for boolean: "%s"' % value)



def epoc_to_datetime(epoc):
    return datetime.fromtimestamp(epoc)

def _pos_neg( pct_change):
    if pct_change > 0:
        return 1
    else:
        return 0

def momentum_quality( ts, min_inf_discr = 0.0, lookback_months = 12, quality_success_ratio = 2 / 3):
    # use momentum quality calculation

    df = pd.DataFrame()

    df['return'] = ts.resample('M').last().pct_change()[-lookback_months:-1]
    if not len(df['return']):
        return False, False

    df['pos_neg'] = df.apply(lambda row: _pos_neg(row['return']) ,axis=1)
    df['pos_sum'] = df['pos_neg'].cumsum()

    positive_sum = 0
    if len(df['pos_sum']) > 0:
        positive_sum = df['pos_sum'].iloc[-1]
        consist_indicator = df['pos_sum'].iloc[-1] >= lookback_months * quality_success_ratio

    if positive_sum == 0:
        pos_percent = 0
        neg_percent = 1
    elif positive_sum >= lookback_months - 1:
         pos_percent = 1
         neg_percent = 0
    else:
        pos_percent, neg_percent = df['pos_neg'].value_counts(normalize=True)
    perc_diff = neg_percent - pos_percent
    print(' > pos sum: {}'.format( positive_sum))
    pret = ((df['return']+1).cumprod()-1).iloc[-1]
    inf_discr =  np.sign(pret) * perc_diff
    if inf_discr < float(min_inf_discr) and consist_indicator:
        return inf_discr, positive_sum, True

    return inf_discr, positive_sum, False

def momentum_score(ts):
    """
    Input:  Price time series.
    Output: Annualized exponential regression slope,
            multiplied by the R2
    """
    # Make a list of consecutive numbers
    x = np.arange(len(ts))
    # Get logs
    log_ts = np.log(ts)
    # Calculate regression values
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, log_ts)
    # Annualize percent
    annualized_slope = (np.power(np.exp(slope), 252) - 1) * 100
    #Adjust for fitness
    score = annualized_slope * (r_value ** 2)
    return score

def volatility(ts, vola_window = 20):
    return ts.pct_change().rolling(vola_window).std().mean()
