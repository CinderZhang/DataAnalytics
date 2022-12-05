# %% download financial ratios from yahoo finance
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import os
import sys
import time
import requests
import json
import re
import math
import warnings
import pickle
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
import statsmodels.stats.api as sms
# %% define functions
def get_financials(ticker, period='5y', interval='1mo'):
  
    # get financials
    # https://pypi.org/project/yfinance/
    stock = yf.Ticker(ticker)

    # Download financials data
    financials = stock.financials
    financials.to_csv(f"{ticker}_financials.csv")

    # Download quarterly financials data
    quarterly_financials = stock.quarterly_financials
    quarterly_financials.to_csv(f"{ticker}_quarterly_financials.csv")

# %% main
if __name__ == '__main__':
    stock = 'AAPL'
    get_financials(stock)

# %%
