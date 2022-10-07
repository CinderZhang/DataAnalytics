
# %%
from codecs import ignore_errors
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

#%% download single file
#df_stk = web.DataReader('AAPL', 'yahoo', start='2019-09-10', end='2019-10-09')

#%% list of stock tickers
stk_list = ["AAPL","GOOG","INTC","F","GM","TSLA","MSFT"]
print(stk_list)

# %% initiate the long format dataframe
#i = 0
long_df =pd.DataFrame()

#%% loop through
for stk in stk_list:
    #print(i)
    print(stk)
    #i = i+1
    df_stk = web.DataReader(stk, 'yahoo', start='2019-09-10', end='2019-10-09')
    print(df_stk.head())
    # Save the stock price data
    #[MASK]
    filename = stk + '.csv'
    #print(filename)
    df_stk.to_csv(filename)
    # Alternatively, combine all stock price info into one long format data file
    df_stk['ticker'] = stk
    long_df = long_df.append(df_stk)
    
    
# %% save
long_df.to_csv("Combined_stock_price.csv",index=False)

# %%
