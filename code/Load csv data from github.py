# load csv data from github
import pandas as pd
url = 'https://raw.githubusercontent.com/CinderZhang/DataAnalytics/main/data/AAPL_CRSP_Daily.csv'
df = pd.read_csv(url)

