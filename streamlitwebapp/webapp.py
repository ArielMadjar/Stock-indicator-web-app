#Import Libraries
import warnings
warnings.filterwarnings('ignore')  # Hide warnings
import datetime as dt
import pandas as pd
import pandas_datareader as web
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st

from PIL import Image
import os
#Importing Libraries done

#import cover image
image = Image.open(os.path.join('cover.png'))
st.image(image,use_column_width=True)

#Set title
st.title('Stock Indicators Web App')
'---------------------------------------------------------'
#text
st.header("Developed by **Ariel Madjar** :boy:")



tic = st.text_input("Enter the ticker symbol of a stock","WIX") #Insert the Ticker Symbol

st.write('You Enterted the stock symbol: ', tic)

st_date= st.text_input("Enter Starting date as YYYY-MM-DD", "2020-01-10")

'You Enterted the starting date: ', st_date

end_date= st.text_input("Enter Ending date as YYYY-MM-DD", "2021-02-09")

'You Enterted the ending date: ', end_date

df = web.DataReader(tic, 'yahoo', st_date, end_date)  # Collects data
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)

#title
st.title('Stock Data')

'The '+ tic +' Stock Data Frame: '
df

tic +' Stock Close Price Chart: '
st.line_chart(df["Close"])

tic + ' Stock Volume: '
st.area_chart(df["Volume"])

#title
st.title('Exponential Moving Averages :chart:')
'---------------------------------------------------------'
'Stock Data Based on Exponential Moving Averages Strategy'
'An Exponential Moving Average (EMA) is a stock indicator that is commonly used in technical analysis.'
st.write("You can read more about EMA strategies in my [Medium Article link](https://arielmadjar.medium.com/understanding-stock-trading-strategies-using-python-285e5069ba3e)")
st.write("For The Golden Cross Strategy use Short EMA:50 Long EMA:200")
ShortEMA= st.text_input("Enter number of days Short Exponential Moving Average:", "9")

LongEMA= st.text_input("Enter number of days a Long Exponential Moving Average:", "50")

'You Enterted the Short Moving Average: ', ShortEMA
'You Enterted the Long Moving Average: ', LongEMA

ColShortEMA= df.Close.ewm(span=int(ShortEMA),adjust=False).mean()
df["ShortEMA"] =ColShortEMA

'1. Plot of Stock Closing Value for '+ ShortEMA+ " Days of Short Exponential Moving Average"
'And ' +LongEMA+ ' Days of Long Exponential Moving Average'
'   Actual Closing Value also Present'

ColLongEMA = df.Close.ewm(span=int(LongEMA),adjust=False).mean()
df["LongEMA"] =ColLongEMA




st.line_chart(df[["ShortEMA","Close","LongEMA"]])

'2. Plot of Stock MACD Line'
MACD = ColShortEMA - ColLongEMA
df["MACD"] = MACD.ewm(span=9,adjust=False).mean()
st.line_chart(df[["Close","MACD"]])


def vis_golden(data):
    plt.figure()
    plt.title(tic + ' Close Price History')
    plt.plot(df['Close'],label='Close Price',alpha=0.5)
    plt.plot(df["ShortEMA"], label='Short EMA',alpha=0.6,color='gold')
    plt.plot(df["LongEMA"], label='Long EMA',alpha=0.6,color='purple')
    plt.scatter(df.index, df['Buy'], color = 'green', marker='^',alpha=1)
    plt.scatter(df.index, df['Sell'], color = 'red', marker='v',alpha=1)
    plt.legend([' Close Price','Short EMA', 'Long EMA','Buy','Sell' ], loc='lower right')
    plt.xlabel('Date',fontsize=15)
    plt.ylabel('Close Price USD ($)',fontsize=15)
    st.pyplot()


def gold_croos_buy(data):
  buy_listG=[]
  sell_listG=[]
  long_flag=False
  short_flag=False

  for i in range(0,len(data)):
      if data['ShortEMA'][i] < data['LongEMA'][i] and long_flag == False and short_flag == False:
        sell_listG.append(data['Close'][i])
        buy_listG.append(np.nan)
        short_flag = True
      elif short_flag == True and data ['ShortEMA'][i] < data ['LongEMA'][i]:
        sell_listG.append(data['Close'][i])
        sell_listG.append(np.nan)
        short_flag  = False
        long_flag = True
      elif long_flag == True and (data ['ShortEMA'][i] > data ['LongEMA'][i]) :
        buy_listG.append(data['Close'][i])
        buy_listG.append(np.nan)
        short_flag  = True
        long_flag = False
      else:
        buy_listG.append(np.nan)
        sell_listG.append(np.nan)


  return (buy_listG,sell_listG)


  
if st.checkbox('View Buy/Sell indicators '):

   df['Buy']= gold_croos_buy(df)[0]
   df['Sell']=gold_croos_buy(df)[1]
   vis_golden(df)