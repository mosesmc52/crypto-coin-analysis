## Conduct analysis on Crypto data

### Data Historical Data CryptoCompare.com
https://min-api.cryptocompare.com/

### Setup
`pipenv install`<br>
`pipenv shell`

Required Environmental Variables<br>
CRYPTO_COMPARE_API_KEY<br>
CRYPTO_COMPARE_HOSTNAME<br>

Files and steps fo execution:<br>
1) coins.py<br>
Downloads all of the existing cryptocoins<br>
2) historical_price_data.py<br>
Downloads historical price data<br>
3) historical_social_data.py<br>
Downloads historical social data<br>
4) coins_that_have_historical_data.py<br>
Filters out coins that have both historical price and social data<br>
5) merge_price_social_data.py<br>
Merges historical price and social data<br>

6) plot.py<br>
Plots coin data for analysis. This file produces two plots a correlation and  time series plot<br>

8) has_trend.py<br>
Detects trends within price data<br>

stats.py<br>
Prints out stats on coin<br>

### Coin Header Fields
Id<br>
Url<br>
ImageUrl<br>
ContentCreatedOn<br>
Name<br>
Symbol<br>
CoinName<br>
FullName<br>
Description<br>
AssetTokenStatus<br>
Algorithm<br>
ProofType<br>
SortOrder<br>
Sponsored<br>
Taxonomy<br>
Rating<br>
IsTrading<br>
TotalCoinsMined<br>
CirculatingSupply<br>
BlockNumber<br>
NetHashesPerSecond<br>
BlockReward<br>
BlockTime<br>
AssetLaunchDate<br>
AssetWhitepaperUrl<br>
AssetWebsiteUrl<br>
MaxSupply<br>
MktCapPenalty<br>
IsUsedInDefi<br>
IsUsedInNft<br>
BuiltOn<br>
DecimalPoints<br>
PlatformType<br>
SmartContractAddress<br>
Difficulty<br>
AlgorithmType<br>

### Price Header Fields
time<br>
high<br>
low<br>
open<br>
volumefrom<br>
volumeto<br>
close<br>

### Social Header Fields
conversionType<br>
conversionSymbol<br>
comments<br>
posts<br>
followers<br>
points<br>
overview_page_views<br>
analysis_page_views<br>
markets_page_views<br>
charts_page_views<br>
trades_page_views<br>
forum_page_views<br>
influence_page_views<br>
total_page_views<br>
fb_likes<br>
fb_talking_about<br>
twitter_followers<br>
twitter_following<br>
twitter_lists<br>
twitter_favourites<br>
twitter_statuses<br>
reddit_subscribers<br>
reddit_active_users<br>
reddit_posts_per_hour<br>
reddit_posts_per_day<br>
reddit_comments_per_hour<br>
reddit_comments_per_day<br>
code_repo_stars<br>
code_repo_forks
code_repo_subscribers<br>
code_repo_open_pull_issues<br>
code_repo_closed_pull_issues<br>
code_repo_open_issues<br>
code_repo_closed_issues<br>
code_repo_contributors<br>
