#%% weighted portfolio returns

import sys
import os
import re
import csv
import datetime
import argparse
import logging
import logging.handlers
import traceback
import collections
import math
import decimal
import pprint

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
#import matplotlib.finance as mfinance
import matplotlib.patches as mpatches
import matplotlib.lines as mlines


#%% Simple example of weighted portfolio returns
wght = [1, -1]
ret = [0.1, 0.2]
print("wght = ", wght)
print("ret = ", ret)
print("np.dot(wght, ret) = ", np.dot(wght, ret))
    

# %% Real example of weighted portfolio returns
# Read in the price data
raw = pd.read_csv('../../source/tr_eikon_eod_data.csv', index_col=0, parse_dates=True).dropna()
symbols = ['AAPL.O', 'MSFT.O'] 
# %% Keep only the selected symbols
data = raw[symbols]
data = data.dropna()
data.info()
# %% Plot the data -- normalized to $100
(data / data.iloc[0] * 100).plot(figsize=(10, 6))

# %% try to calculate the returns
rets = np.log(data / data.shift(1))
rets.head()
# %% Plot the returns
rets.plot(figsize=(16, 10), subplots=True)





# %% Calculate the weighted portfolio returns
wght = [0.5, 0.5]
retp=rets[symbols]
retp['Portfolio'] = np.dot(retp, wght)
retp.dropna(inplace=True)
retp.head()
# %% Plot the portfolio returns
retp[['Portfolio']].plot(figsize=(10, 6))
# %% portfolio returns statistics
retp.describe()
retp.describe()
print("Annualized Return\n",retp.mean() * 252)
print("Annualized Volatility\n",retp.std() * np.sqrt(252))

# %% Calculate the long-short portfolio returns
wght = [1, -1]
retls=rets[symbols]
retls['Portfolio'] = np.dot(retls, wght)
retls.dropna(inplace=True)
retls.head()
# %% Plot the long-short portfolio returns
retls[['Portfolio']].plot(figsize=(10, 6))
# %% Calculate the long-short portfolio returns statistics
retls.describe()
print("Long-Short Annualized Return\n",retls.mean() * 252)
print("Long-Short Annualized Volatility\n",retls.std() * np.sqrt(252))

# %%
