# -*- coding: utf-8 -*-
"""
Spyder Editor

CAPM/FF factor models script file.
"""

   
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
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

# %%
def price2ret(prices,retType='simple'):
    if retType == 'simple':
        ret = (prices/prices.shift(1))-1
    else:
        ret = np.log(prices/prices.shift(1))
    return ret


# %%
def assetPriceReg(df_stk):
    import pandas_datareader.data as web  # module for reading datasets directly from the web
    
    # Reading in factor data
    df_factors = web.DataReader('F-F_Research_Data_5_Factors_2x3_daily', 'famafrench')[0]
    df_factors.rename(columns={'Mkt-RF': 'MKT'}, inplace=True)
    df_factors['MKT'] = df_factors['MKT']/100
    df_factors['SMB'] = df_factors['SMB']/100
    df_factors['HML'] = df_factors['HML']/100
    df_factors['RMW'] = df_factors['RMW']/100
    df_factors['CMA'] = df_factors['CMA']/100
    
    df_stock_factor = pd.merge(df_stk,df_factors,left_index=True,right_index=True) # Merging the stock and factor returns dataframes together
    df_stock_factor['XsRet'] = df_stock_factor['Returns'] - df_stock_factor['RF'] # Calculating excess returns

    # Running CAPM, FF3, and FF5 models.
    CAPM = sm.ols(formula = 'XsRet ~ MKT', data=df_stock_factor).fit(cov_type='HAC',cov_kwds={'maxlags':1})
    FF3 = sm.ols( formula = 'XsRet ~ MKT + SMB + HML', data=df_stock_factor).fit(cov_type='HAC',cov_kwds={'maxlags':1})
    FF5 = sm.ols( formula = 'XsRet ~ MKT + SMB + HML + RMW + CMA', data=df_stock_factor).fit(cov_type='HAC',cov_kwds={'maxlags':1})

    CAPMtstat = CAPM.tvalues
    FF3tstat = FF3.tvalues
    FF5tstat = FF5.tvalues

    CAPMcoeff = CAPM.params
    FF3coeff = FF3.params
    FF5coeff = FF5.params

    # DataFrame with coefficients and t-stats
    results_df = pd.DataFrame({'CAPMcoeff':CAPMcoeff,'CAPMtstat':CAPMtstat,
                               'FF3coeff':FF3coeff, 'FF3tstat':FF3tstat,
                               'FF5coeff':FF5coeff, 'FF5tstat':FF5tstat},
    index = ['Intercept', 'MKT', 'SMB', 'HML', 'RMW', 'CMA'])


    dfoutput = summary_col([CAPM,FF3, FF5],stars=True,float_format='%0.4f',
                  model_names=['CAPM','FF3','FF5'],
                  info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                             'Adjusted R2':lambda x: "{:.4f}".format(x.rsquared_adj)}, 
                             regressor_order = ['Intercept', 'MKT', 'SMB', 'HML', 'RMW', 'CMA'])

    print(dfoutput)
    
    return results_df


# %%

df_stk = web.DataReader('AAPL', 'yahoo', start='2019-09-10', end='2019-10-09')

# home = str(Path.home())
# print(home)


# # %%


# if sys.platform == 'linux':
#     inputDir = '/datasets/stocks/' 
# elif sys.platform == 'win32':
#     inputDir = '\\datasets\stocks\\' 
# else :
#     inputDir = '/datasets/stocks/'
    
# fullDir = home+inputDir
# print(fullDir)


# # %%
# stkName = 'AAPL'
# fileName = 'stk_' + stkName + '.csv'
# readFile = fullDir+fileName 

# df_stk = pd.read_csv(readFile,index_col='Date',parse_dates=True)
df_stk.head()


# %%
df_stk.drop(['Volume'],axis=1,inplace=True)
df_stk.plot()


# %%
df_stk['Returns'] = price2ret(df_stk[['Adj Close']])
df_stk = df_stk.dropna()
df_stk.head()


# %%
df_stk['Returns'].plot()


# %%
df_stk['Returns'].hist(bins=20)


# %%
df_regOutput = assetPriceReg(df_stk)
# xlsfile=fullDir+stkName+'_CAPM_FF.xlsx'
# print(xlsfile)

# # %% output model
# df_regOutput.to_excel(xlsfile)
