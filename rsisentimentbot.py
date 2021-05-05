# Jason Bonilla
# Live sentiment analysis trading bot that uses an rsi technical indicator strategy
import praw
import config
from textblob import TextBlob
from binance.client import Client
from binance.enums import *
from ta.momentum import RSIIndicator
import pandas as pd

# passing API key and API secret from BINANCE
client = Client(config.BINANCE_KEY, config.BINANCE_SECRET, tld='us')

# configuring the python Reddit API wrapper
reddit = praw.Reddit(
    client_id= config.REDDIT_ID,
    client_secret= config.REDDIT_SECRET,
    password= config.REDDIT_PASS,
    user_agent="USERAGENT",
    username= config.REDDIT_USER,
)

sentimentList= []
dogePrices = []
neededSentiments = 300

TRADE_SYMBOL = 'DOGEUSDT'
TRADE_QUANTIY = 0.0001
# upper amd lower bands to help indicate if stock is overbought or oversold
UPPER_BAND = 70
LOWER_BAND = 30

# ensures that the coin is not being bought repeatedly 
# waits until a sell signal is recieved in order to proceed
in_position = False

# returns average of sentiment list after 300 comments
def Average(lst):
    if len(lst) == 0:
        return len(lst)
    else:
        return sum(lst[-neededSentiments:]) / neededSentiments

# most essential part of this bot, repsonisble for executing orders
# side = buy or sell 
# quantity = how many of a coin 
# symbol = currecy pair that is being traded (BTC, Doge UTC, Doge BTC, etc. )
def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        PRINT('SENDING ORDER')
        order = client.create_order(symbol=symbol, side =side, type = order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print('an exception has occured '+ e)
        return False
    return True


# will print the polarity and subjectivity of each comment in the stream.
# 0 means neutral, <0 means negative sentiment and >0 means positive sentiment
# if the average polarity is not neutral then a trade is excecuted  
for comment in reddit.subreddit("dogecoin").stream.comments():

    redditComment = comment.body
    blob = TextBlob(redditComment)

    sent = blob.sentiment
    #print("************** Sentiment is: "+ str(sent.polarity))

    # any value besides 0 will be used to find out average
    if sent.polarity != 0.0:
        sentimentList.append(sent)
        
        # nested lists that gives most recent prices of dogecoin formatted: open, high, low, close
        # focus on the open price because it tends to moves less
        candles = client.get_historical_klines(TRADE_SYMBOL, Client.KLINE_INTERVAL_5MINUTE, "5 Minutes ago UTC")
        # print(candles[-1][1])

        # if dogePrices is empty append to list else
        # if last value of dogePrices does not equal last value of candles then we append it\
        # ensures unique data
        if len(dogePrices) == 0:
            dogePrices.append(float(candles[-1][1]))
        elif dogePrices[-1] != float(candles[-1][1]): 
            dogePrices.append(float(candles[-1][1])) 

        # compares the magnitude of recent gains and losses over a specified time period to 
        # measure speed and change of price movements of a security. RSI is primarily used to 
        # attempt to identify overbought or oversold conditions in the trading of an asset.
        rsi = RSIIndicator(pd.Series(dogePrices))
        df = rsi.rsi()
        print(rsi.rsi())

        # holds last rsi value and indicates if stock is overbought or oversold
        # if >70 then overbought -> sell
        # if <30 then oversold -> buy
        df.iloc[-1]

        if(df.iloc[-1] <LOWER_BAND and len(sentimentList) > neededSentiments and round(Average(sentimentList)) > -0.5 ):
             if in_position:
                print(" ************* BUY ORDER BUT WE OWN ************* ")
            else:
                 print(" ************* BUY ORDER  ************* ")
                 order_succeeded = order(SIDE_BUY, TRADE_QUANTIY, TRADE_SYMBOL)
                 if order_succeeded:
                    in_position = True
        elif(df.iloc[-1] > UPPER_BAND and len(sentimentList) > neededSentiments and round(Average(sentimentList)) < -0.5):
             if in_position:
                order_succeeded = order(SIDE_SELL, TRADE_QUANTIY, TRADE_SYMBOL)
                if order_succeeded:
                    in_position = False
                else:
                    print("************* SELL ORDER BUT WE DONT OWN *************")
