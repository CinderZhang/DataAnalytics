#%%
import pandas as pd
import requests
#%%
csv_url = "https://raw.githubusercontent.com/CinderZhang/DataAnalytics/main/data/DGS5.csv"
#csv_content = requests.get(csv_url).content
print(csv_url)

#%%
dgs5_df = pd.read_csv(csv_url,index_col="DATE",parse_dates=True)

# %%
dgs5_df.dtypes
# %%
dgs5_df['DGS5'] = pd.to_numeric(dgs5_df['DGS5'],errors='coerce')
# %%
dgs5_df.dtypes
# %%
