# read csv file from github
import pandas as pd
url = 'https://github.com/CinderZhang/DataAnalytics/blob/main/data/AAPL_CRSP_Daily.csv'
df = pd.read_csv(url)
