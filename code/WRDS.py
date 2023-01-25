#!pip install wrds
#https://github.com/wharton/wrds
# %% WRDS, need to install wrds package first
import wrds
# need username and password
db = wrds.Connection(wrds_username='joe')
db.create_pgpass_file()
# %% read data
params = {"tickers": ("AAPL", "WMT")}
financial_data = db.raw_sql(
    "SELECT tic, datadate, gvkey, cusip FROM comp.funda WHERE tic IN %(tickers)s",
    params=params,
)
# %% 
stk_prc = db.raw_sql(
    "SELECT * FROM crspa.crsp_a_stock WHERE ticker IN %(tickers)s ",
    params=params,
)
# %%
