#!pip install wrds
#https://github.com/wharton/wrds
# %% WRDS, need to install wrds package first
import wrds

############################################
### need username and password  ###
############################################
db = wrds.Connection(wrds_username='joe')
db.create_pgpass_file()

# %% read stock price and return data, AAPL's permno is 14593
# %%
apple = db.raw_sql("""select permno, date, prc, ret, shrout 
                        from crsp.msf 
                        where permno = 14593
                        and date>='01/01/2019'""", 
                     date_cols=['date'])# %% read financial data
# %% read financial data
params = {"tickers": ("AAPL")}
financial_data = db.raw_sql(
    "SELECT tic, datadate, gvkey, cusip FROM comp.funda WHERE tic IN %(tickers)s",
    params=params,
)
