#%%
# %%
import pandas as pd
import numpy as np 
import pandas_datareader.data as web 
import statsmodels.formula.api as sm # module for stats models
from statsmodels.iolib.summary2 import summary_col # module for presenting stats models outputs nicely
from pathlib import Path
import sys
import os
import pandas_datareader as pdr
import datetime as dt

import matplotlib.pyplot as plt
# %%
def price2ret(prices,retType='simple'):
    if retType == 'simple':
        ret = (prices/prices.shift(1))-1
    else:
        ret = np.log(prices/prices.shift(1))
    return ret

#%% read in stock data
df_stk = web.DataReader('AAPL', 'yahoo', start='2020-03-10', end='2022-09-09')

#%% Plot stock data
df_stk.drop(['Volume'],axis=1,inplace=True)
df_stk.plot()



# %% Prepare for regression
df_stk['Returns'] = price2ret(df_stk[['Adj Close']])
df_stk = df_stk.dropna()
df_stk.head()

#%% Reading in factor data
df_factors = web.DataReader('F-F_Research_Data_5_Factors_2x3_daily', 'famafrench')[0]
df_factors.rename(columns={'Mkt-RF': 'MKT'}, inplace=True)

 #%%
df_factors['MKT'] = df_factors['MKT']/100
df_factors['SMB'] = df_factors['SMB']/100
df_factors['HML'] = df_factors['HML']/100
df_factors['RMW'] = df_factors['RMW']/100
df_factors['CMA'] = df_factors['CMA']/100
    
#%%
df_stock_factor = pd.merge(df_stk,df_factors,left_index=True,right_index=True) # Merging the stock and factor returns dataframes together
df_stock_factor['XsRet'] = df_stock_factor['Returns'] - df_stock_factor['RF'] # Calculating excess returns

# %% plot data
df_stock_factor['MKT'].plot()
df_stock_factor['Returns'].plot()

# %% scatter plot
plt.scatter(x=df_stock_factor['MKT'], y=df_stock_factor['Returns']);
#%% Sample for simple regression
sample = df_stock_factor[['MKT' , 'Returns']]

#%% correlation
sample.corr()
# %% Regression/Trend line
reg = np.polyfit(sample['MKT'], sample['Returns'], deg = 1)
#%% Plot regression trend line
trend = np.polyval(reg, sample['MKT'])
plt.scatter(sample['MKT'], sample['Returns'])
plt.plot(sample["MKT"], trend, 'r');
plt.axvline(0, c='black', ls='--')
plt.axhline(0, c='black', ls='--')
# %%
