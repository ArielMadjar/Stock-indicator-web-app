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

import cufflinks as cf
import yfinance as yf
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
#st.header("Developed by **Ariel Madjar** :boy:")



tic = st.text_input("Enter the ticker symbol of a stock","WIX") #Insert the Ticker Symbol

tickerData = yf.Ticker(tic)


st.write('You Enterted the stock symbol: ', tic)

string_logo = '<img src=%s>' % tickerData.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)

#st_date= st.("Enter Starting date as YYYY-MM-DD", "2020-01-10")

st_date = st.date_input("Start date", dt.date(2019, 1, 1))
end_date = st.date_input("End date", dt.date(2021, 1, 31))

'You Enterted the starting date: ', st_date

#end_date= st.text_input("Enter Ending date as YYYY-MM-DD", "2021-02-09")

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
st.write("For The ** Golden Cross Strategy ** use Short EMA: **50** Long EMA:** 200 **")
ShortEMA= st.text_input("Enter number of days Short Exponential Moving Average:", "9")

LongEMA= st.text_input("Enter number of days a Long Exponential Moving Average:", "50")

'You Enterted the Short Moving Average: ', ShortEMA
'You Enterted the Long Moving Average: ', LongEMA

ColShortEMA= df.Close.ewm(span=int(ShortEMA),adjust=False).mean()
df["ShortEMA"] =ColShortEMA 

'Plot of Stock Closing Value for '+ ShortEMA+ " Days of Short Exponential Moving Average"
'And ' +LongEMA+ ' Days of Long Exponential Moving Average'
'   Actual Closing Value also Present'

ColLongEMA = df.Close.ewm(span=int(LongEMA),adjust=False).mean()
df["LongEMA"] =ColLongEMA




st.line_chart(df[["ShortEMA","Close","LongEMA"]])

#'2. Plot of Stock MACD Line'
#MACD = ColShortEMA - ColLongEMA
#df["MACD"] = MACD.ewm(span=9,adjust=False).mean()
#st.line_chart(df[["Close","MACD"]])


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



if st.checkbox('View Golden Cross Buy/Sell indicators'):

   df['Buy']= gold_croos_buy(df)[0]
   df['Sell']=gold_croos_buy(df)[1]
   vis_golden(df)



strg_name = st.selectbox("Select Strategy",("RSI","MACD","ADX","Bollinger Bands","Complex View"))

if strg_name=="Bollinger Bands":
  
  st.header('**Bollinger Bands**')
  qf=cf.QuantFig(df,title='First Quant Figure',legend='top',name='GS')
  qf.add_bollinger_bands()
  fig = qf.iplot(asFigure=True)
  st.plotly_chart(fig)
elif strg_name=="RSI":
  st.header("**RSI**")
  rsi_period=st.slider("RSI Periods",10,100,20,10)
  qf=cf.QuantFig(df,title='RSI',legend='top',name='GS')
  qf.add_rsi(periods=rsi_period, rsi_upper=70, rsi_lower=30, showbands=True, column=None, name=tickerData.info['longName'], str=None)
  fig = qf.iplot(asFigure=True)
  st.plotly_chart(fig)
elif strg_name=="ADX":
  st.header("**ADX**")
  adx_period=st.slider("ADX Periods",1,50,14,1)
  qf=cf.QuantFig(df,kind='candlestick',title="ADX",legend = 'top')
  qf.add_adx(periods=adx_period)
  fig = qf.iplot(asFigure=True)
  st.plotly_chart(fig)
elif strg_name=="MACD":
  st.header("**MACD**")
  qf=cf.QuantFig(df,kind='candlestick',title="MACD",legend = 'top')
  qf.add_macd()
  fig = qf.iplot(asFigure=True)
  st.plotly_chart(fig)
elif strg_name=="Complex View":
  #df=cf.datagen.ohlc()
  rsi_period=st.slider("RSI Periods",10,100,20,10)
  qf=cf.QuantFig(df,title='First Quant Figure',legend='top',name='GS')
  #qf=cf.QuantFig(df,kind='candlestick',title="Complex View",legend = 'top'
  qf.add_sma([10,20],width=2,color=['green','lightgreen'],legendgroup=True)
  qf.add_rsi(periods=rsi_period,color='java')
  qf.add_bollinger_bands(periods=20,boll_std=2,colors=['magenta','grey'],fill=True)
  #qf.add_volume(colorchange=True,column=None,name='Volume',str='')
  qf.add_macd()
  fig = qf.iplot(asFigure=True)
  st.plotly_chart(fig)
  #qf.iplot()





  

  
