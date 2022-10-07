
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

#%% download single file
#df_stk = web.DataReader('AAPL', 'yahoo', start='2019-09-10', end='2019-10-09')

#%% list of stock tickers
stk_list = ["AAPL","GOOG","INTC"]
print(stks)

# %%
i = 0
for stk in stk_list:
    print(i)
    print(stk)
    i = i+1
    df_stk = web.DataReader(stk, 'yahoo', start='2019-09-10', end='2019-10-09')
    print(df_stk.head())
    # Save the stock price data
    #[MASK]
    filename = stk + '.csv'
    #print(filename)
    df_stk.to_csv(filename)
#%% combine all stock price info into one long format data file
# %%

# %%
