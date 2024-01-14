#!pip install wrds
#https://github.com/wharton/wrds
# %% WRDS, need to install wrds package first
import wrds
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
############################################
### need username and password  ###
############################################
db = wrds.Connection(wrds_username='cinderuark')
db.create_pgpass_file()

# %% read stock price and return data, AAPL's permno is 14593

apple_stk_monthly = db.raw_sql("""select *
                        from crsp.msf 
                        where permno = 14593
                        and date>='01/01/2019'""", 
                     date_cols=['date'])



# %% read financial data
apple_fin = db.raw_sql("""select *
                        from comp.funda
                        where tic = 'AAPL'
                        """, 
                     date_cols=['datedate'])


# params = {"tickers": ("AAPL")}

# financial_data = db.raw_sql(
#     "SELECT tic, datadate, gvkey, cusip,at FROM comp.funda WHERE tic IN %(tickers)s",
#     params=params,
# )

# %% Fama French 5 factors
ff_monthly = db.raw_sql("""select *
                        from ff.	fivefactors_monthly 
                        where date>='01/01/2019'""", 
                     date_cols=['date'])
                     

# %% lagged return
apple_stk_monthly['return'] = apple_stk_monthly['ret'].shift(1)

# %% lagged Fama French 5 factors
ff_monthly['lagged_mktrf'] = ff_monthly['mktrf'].shift(1)
ff_monthly['lagged_smb'] = ff_monthly['smb'].shift(1)
ff_monthly['lagged_hml'] = ff_monthly['hml'].shift(1)
ff_monthly['lagged_rmw'] = ff_monthly['rmw'].shift(1)
ff_monthly['lagged_cma'] = ff_monthly['cma'].shift(1)


# %% merge data ff_daily and apple_stk_daily
apple_stk_ff_monthly = pd.merge(apple_stk_monthly, ff_monthly, on='date', how='left')



# %%
