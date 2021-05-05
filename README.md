# Reddit Trading Bot 2
Live sentiment analysis trading bot that handles cryptocurrencies specifically
Dogecoin, based off the overall sentiment of live comments under r/dogecoin
using an [rsi technical indicator](https://www.investopedia.com/terms/r/rsi.asp) strategy

## Requirements
- Must have [PRAW](https://praw.readthedocs.io/en/latest/) installed
- Must have [TextBlob](https://textblob.readthedocs.io/en/dev/) installed
- Must have [python-binance](https://python-binance.readthedocs.io/en/latest/) installed
- Must have at least [python3.6](https://www.python.org/downloads/) installed 
- Must have [conda](https://conda.io/projects/conda/en/latest/user-guide/install/windows.html) installed 

## Instructions
Create a virtual environment using conda:
- **create --name ENVNAME python=3.6**

Run virtual environment using conda:
- **conda activate ENVNAME**

Fill in config.py with your own personal Reddit username API ID/Secret, and Binance API KEY/Secret
- [How to create Binance API Key](https://www.binance.com/en/support/faq/360002502072)
- [How to create Reddit API Key](https://github.com/reddit-archive/reddit/wiki/OAuth2)

Specify which cryptocurrency you would like to trade and the bounds for the RSI. The code is preset to [Dogecoin(DOGE)](https://dogecoin.com/), an upperbound of 70, and a lowerbound of 30. In order to switch coins and/or follow a non-traditional rsi strategy, the folowing need to be changed accordingly:
- **TRADE_SYMBOL**
- **reddit.subreddit()**
- **UPPER_BAND**
- **LOWER_BAND**

Run program:
- **python rsisentimentbot.py**
