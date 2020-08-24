import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

stocks = ["AMZN", "MSFT", "AAPL", "GOOG"]
start = datetime.datetime.today() - datetime.timedelta(30)
end = datetime.datetime.today()
cl_price = pd.DataFrame() #empty dataframe which will be filled with closing prices
ohlcv_data = {}

#looping over tickers and creating a dataframe with close prices
for ticker in stocks:
    cl_price[ticker] = yf.download(ticker, start, end)["Adj Close"]

#looping over tickers and creating a dataframe with the WHOLE dataframe
for ticker in stocks:
    ohlcv_data[ticker] = yf.download(ticker, start, end)


#Filling nan valueS
#Arguments for .fillna() can also include methods - where the result of the
#method can determine the fill value. You can also use dictionary key value 
#pairs to set a fill value for an individual stock {"AMZN": 0}
    
#Note: filling nan values is prefered to just dropping nan values
cl_price.fillna(method='bfill', axis=0, inplace=True)

#Dropping nan values - deletes any row where NaN value exists
cl_price.dropna(axis=0, inplace=True)

#Mean, Median, Standard Deviation, daily return
print("Close Price Mean:")
print (cl_price.mean())
print("Close Price Median:")
print (cl_price.median())
print("Close Price Standard Deviation:")
print (cl_price.std())

#Gives the percentage return for the given time period
daily_return = cl_price.pct_change()
print("Stock daily return with mean and std:")
print (daily_return)
print (daily_return.mean())
print (daily_return.std()) 

#Calc rolling averages for the given time window
print(daily_return.rolling(window=20).mean())
print(daily_return.rolling(window=20).std())

#Exponential moving average
print(daily_return.ewm(span=20, min_periods=20).mean())


#Data Visualisation - This is used to display data in an easy
#to understand way.
cl_price.plot()

#Standardisation creates a Z-value for each stock, this essentially puts all
#the stock into the same range.s
cl_price_standardised = (cl_price - cl_price.mean()) / cl_price.std()
#Pay attention to use of .plot arguments - more can be found by searching
#pandas.DataFrame.plot() online.
cl_price_standardised.plot(subplots=True, layout=(3,2), title="Standardised stock prices")

#Note: You can also use matplotlib.pyplot - this is the method used at University
#to visualise data.
# Pyplot demo
fig, ax = plt.subplots()
plt.style.available
plt.style.use('ggplot')
ax.set(title="Daily return on tech stocks", xlabel="Tech Stocks", ylabel = "Daily Returns")
plt.bar(daily_return.columns,daily_return.mean())