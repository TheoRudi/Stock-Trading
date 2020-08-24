# =============================================================================
# Import OHLCV data and calculate RSI technical indicators
# Author : Mayank Rasu

# Please report bug/issues in the Q&A section
# =============================================================================

# Import necesary libraries
import pandas as pd
import yfinance as yf
import numpy as np
import datetime as dt
import re
import time

# Download historical data for required stocks
#ticker = "BA"
tickers = []
currencyPairs = []
rsiList = []

def readTickers(exchangeFilePath):
    file_path = exchangeFilePath
    lines = open(file_path,'r').readlines()
    for l in lines[1:]:
        if re.split(r'\t+', l)[0] not in tickers:
            tickers.append(re.split(r'\t+', l)[0])
            
def readCurrencyPair(currencyFilePath):
    file_path = currencyFilePath
    lines = open(file_path,'r').readlines()
    for l in lines[1:]:
        if re.split(r' \t+', l)[0] not in currencyPairs:
            currencyPairs.append(re.split(r' \t+', l)[0])

#readTickers("../Stock_Exchanges/NASDAQX.txt")
readCurrencyPair("../Currency_Pairs.txt")
#DF is the Data frame, n is the number of periods you wish to calc RSI of.
def RSI(DF,n):
    "function to calculate RSI"
    df = DF.copy()
    df['delta']=df['Adj Close'] - df['Adj Close'].shift(1)
    df['gain']=np.where(df['delta']>=0,df['delta'],0)
    df['loss']=np.where(df['delta']<0,abs(df['delta']),0)
    avg_gain = []
    avg_loss = []
    gain = df['gain'].tolist()
    loss = df['loss'].tolist()
    for i in range(len(df)):
        if i < n:
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == n:
            avg_gain.append(df['gain'].rolling(n).mean().tolist()[n])
            avg_loss.append(df['loss'].rolling(n).mean().tolist()[n])
        elif i > n:
            avg_gain.append(((n-1)*avg_gain[i-1] + gain[i])/n)
            avg_loss.append(((n-1)*avg_loss[i-1] + loss[i])/n)
    df['avg_gain']=np.array(avg_gain)
    df['avg_loss']=np.array(avg_loss)
    df['RS'] = df['avg_gain']/df['avg_loss']
    df['RSI'] = 100 - (100/(1+df['RS']))
    return df['RSI']

# Calculating RSI without using loop
def rsi(df, n):
    "function to calculate RSI"
    delta = df["Adj Close"].diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[n-1]] = np.mean( u[:n]) # first value is average of gains
    u = u.drop(u.index[:(n-1)])
    d[d.index[n-1]] = np.mean( d[:n]) # first value is average of losses
    d = d.drop(d.index[:(n-1)])
    rs = u.ewm(com=n,min_periods=n).mean()/d.ewm(com=n,min_periods=n).mean()
    return 100 - 100 / (1+rs)

#print(rsi(ohlcv, 20))
#ohlcv = yf.download(ticker,dt.date.today()-dt.timedelta(1825),dt.datetime.today())

rsiList = {}
overSoldStocks = []
breakthroughStocks = []
for ticker in tickers:
    ohlcv = yf.download(ticker,dt.date.today()-dt.timedelta(1825),dt.datetime.today())
    print(ticker)
    tickerRSI = RSI(ohlcv, 14)
    if(len(tickerRSI) <=5):
        continue
    mostRecentRSI = tickerRSI[len(tickerRSI) -1]
    rsiList[ticker] = mostRecentRSI
    print(mostRecentRSI)
    if mostRecentRSI < 30:
        overSoldStocks.append(ticker)
    elif mostRecentRSI <= 35 and mostRecentRSI >= 30:
        #Check to see if RSI has been below 30 in past 4 periods (ie going up, instead of going down)
        if (tickerRSI[len(tickerRSI) -5] <= 30 or tickerRSI[len(tickerRSI) -4] <= 30 
        or tickerRSI[len(tickerRSI) -3] <= 30 or tickerRSI[len(tickerRSI) -2] <= 30):
            breakthroughStocks.append(ticker)
            
print("")
print("Oversold Stocks:")
for ticker in overSoldStocks:
    print(ticker + "\t" + str(rsiList[ticker]))
    
print("")
print("Breakthrough Stocks:")
for ticker in breakthroughStocks:
    print(ticker + "\t" + str(rsiList[ticker]))

fileName = "Breakthrough_Stocks_RSI_" + str(time.time()) + ".txt"
text_file = open(fileName, "w")
text_file.write("Breakthrough Stocked Based on 30 < RSI >= 35 \n")
for ticker in breakthroughStocks:
    text_file.write(ticker + "\t" + str(rsiList[ticker]) + "\n")

text_file.close()