
#load virtual environment
pipenv shell

# retrieve all coins
python coins.py

# retrieve historical price data
python historical_price_data.py

# retrieve social data
python historical_social_data.py

# filter out only coins that have historical price data
python coins_that_have_historical_data.py

# merge price and social data
python merge_price_social_data.py

# detect trends in data and report
python has_trend.py
