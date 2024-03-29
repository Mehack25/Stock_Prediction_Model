# -*- coding: utf-8 -*-
"""stock prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12F_0RZEbq8ZdzMm-eBYf44wYsj68is3K
"""

##Machine Learning software to predict the prices of stock

!pip install yfinance
!pip install -q xlrd
!pip install mpl_finance
!pip install keras.models
!pip install keras.layers
!pip install sklearn.preprocessing

import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
from pandas import ExcelWriter
from google.colab import drive
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ohlc
import math
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

yf.pdr_override()

##Choose stocks and starting date of your dataset

stock=input("ENter symbol")
sy=int(input("Year from which you want to check"))
sm=1
sd=1
start=dt.datetime(sy,sm,sd)
now=dt.datetime.now()
n=int(input("How many days of data do you wish to use"))
df=pdr.get_data_yahoo(stock,start,now)
plt.figure(figsize=(16,8))
plt.title('Close price History')
plt.plot(df['Close'])
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price USD($)', fontsize=18)
plt.show()
## wokring of model and data
data=df.filter(['Close'])
dataset=data.values
training_data_len=math.ceil(len(dataset)*0.8)
#scaling the data now
scaler=MinMaxScaler(feature_range=(0,1))
scaled_data=scaler.fit_transform(dataset)
#train the data now
train_data=scaled_data[0:training_data_len,:]
#split the data now
x_train=[]
y_train=[]

for i in range(n,len(train_data)):
  x_train.append(train_data[i-n:i,0])
  y_train.append(train_data[i,0])
x_train,y_train=np.array(x_train),np.array(y_train)
x_train=np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1)) #Reshaping because LSTM takes 3d objects only
model=Sequential()
model.add(LSTM(200,return_sequences=True, input_shape=(x_train.shape[1],1)))
model.add(LSTM(200,return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))
model.compile(optimizer='adam',loss='mean_squared_error')
model.fit(x_train,y_train,batch_size=1,epochs=1)
#creating the testing dataset
test_data=scaled_data[training_data_len-n:,:]
x_test=[]
y_test=dataset[training_data_len:,:]
for i in range(n,len(test_data)):
  x_test.append(test_data[i-n:i,0])
x_test=np.array(x_test)
x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))
#get the models predicted price values
predictions=model.predict(x_test)
predictions=scaler.inverse_transform(predictions)

#rmse calculate
rmse=np.sqrt(np.mean(predictions-y_test)**2)
print("The root mean squared error is",rmse)

train=data[:training_data_len]
valid=data[training_data_len:]
valid['Predictions']=predictions
plt.figure(figsize=(16,8))
plt.title('Model')
plt.plot(train['Close'])
plt.plot(valid[['Close','Predictions']])
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price USD($)', fontsize=18)
plt.legend(['Train','Val','Predictions'],loc='lower right')
plt.show()

valid
