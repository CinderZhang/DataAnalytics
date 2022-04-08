# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 21:54:49 2022

@author: cinde
"""

from sec_api import QueryApi


from sec_api import ExtractorApi

import pandas as pd
import json

queryApi = QueryApi(api_key="Your API Key")

query = {
  "query": { "query_string": { 
      "query": "ticker:TSLA AND filedAt:{2020-01-01 TO 2020-12-31} AND formType:\"10-Q\"" 
    } },
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
}

filings = queryApi.get_filings(query)

#print(filings)


df =pd.json_normalize(filings['filings'])


# %% 10-Q extract item 2 

extractorApi = ExtractorApi("Your API Key")   
#filing_url_10q = "https://www.sec.gov/Archives/edgar/data/1318605/000156459020047486/tsla-10q_20200930.htm"
filing_url = df['linkToFilingDetails'][0]
print(filing_url)
section_10q_item2 = extractorApi.get_section(filing_url, "2", "text")

### Problem: Return "undefined"
print(section_10q_item2)

with open('f:\\TSLA_10q_item2.txt', 'w') as f:
    f.write(section_10q_item2)
    