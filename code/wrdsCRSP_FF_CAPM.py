# import wrds package
import wrds
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
import statsmodels.tsa.stattools as ts

# connect to WRDS
conn = wrds.Connection()

# get CRSP data from WRDS
crsp = conn.raw_sql("""
                        select a.permno, a.date, a.ret, a.shrout, b.shrcd, b.exchcd
                        from crsp.dsf as a
                        left join crsp.dsenames as b
                        on a.permno=b.permno and a.date=b.namedt
                        where b.exchcd between 1 and 3 and b.shrcd between 10 and 11
                        """)
# convert date to datetime format
crsp['date'] = pd.to_datetime(crsp['date'])
# get Fama-French data from WRDS
ff = conn.raw_sql("""
                        select date, mktrf, smb, hml, rf
                        from famafrench.factors_daily
                        where date>='01/01/1963'
                        """)
# convert date to datetime format
ff['date'] = pd.to_datetime(ff['date'])
# merge CRSP and Fama-French data
crsp = pd.merge(crsp, ff, on='date')
# run CAPM regression
crsp['retx'] = crsp['ret'] - crsp['rf']
crsp['mktrfx'] = crsp['mktrf'] - crsp['rf']
results = smf.ols('retx ~ mktrfx', data=crsp).fit()
print(results.summary())

# plot regression results
plt.figure(figsize=(10, 6))
plt.scatter(crsp['mktrfx'], crsp['retx'], alpha=0.1)
plt.plot(crsp['mktrfx'], results.params[0] + results.params[1] * crsp['mktrfx'], 'r', lw=2)
plt.xlabel('Market excess return')
plt.ylabel('Excess return')
plt.title('CAPM regression')
plt.show()

