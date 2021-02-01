# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ## Reference
# * https://pbpython.com/record-linking.html

# %%

import wrds
import numpy as np
import pandas as pd
from pathlib import Path
import fuzzymatcher
import recordlinkage


# %%
db = wrds.Connection(wrds_username='cinderuark')
#db.raw_sql('SELECT date,dji FROM djones.djdaily')
parm = {'tickers': ('0015B', '0030B', '0032A', '0033A', '0038A')}
data = db.raw_sql('SELECT datadate,gvkey,cusip FROM comp.funda WHERE tic in %(tickers)s', params=parm)
data


# %%
# Only need to do once to save the credential
# db.create_pgpass_file()


# %%
#db.close()
#db = wrds.Connection(wrds_username='cinderuark')


# %%
#db.list_libraries()


# %%
# Tables in Dealscan
dealscan_tbs=db.list_tables(library='tr_dealscan')
dealscan_tbs


# %%
# dealscan companies
dealscan_comp=db.raw_sql('SELECT * FROM tr_dealscan.company')


# %%
dealscan_comp.head(2)


# %%
#FISD issuers
fisd_issuer=db.raw_sql("select * from fisd.fisd_mergedissuer")


# %%
fisd_issuer.head(2)


# %%
# Columns to match on from fisd as left table
fisd_on = ["legal_name", "city", "state","zipcode","country","sic_code"]

# Columns to match on from df_right
dealscan_on = [
    "company",  "city","state","zipcode","country","primarysiccode"
]


# %%
# Now perform the match
# It will take several minutes to run on this data set
matched_results = fuzzymatcher.fuzzy_left_join(fisd_issuer,
                                               dealscan_comp,
                                               fisd_on,
                                               dealscan_on,
                                               left_id_col='issuer_id',
                                               right_id_col='companyid')


# %%
# Let's see the best matches
sorted_match=matched_results.sort_values(by=['best_match_score'], ascending=False)


# %%
sorted_match


# %%
##Save as CSV file
sorted_match.to_csv('fisd_dealscan_name_match.csv', index=False, compression='zip')


# %%
matched_results.query("best_match_score >= 0.5").sort_values(
    by=['best_match_score'], ascending=False)


# %%



