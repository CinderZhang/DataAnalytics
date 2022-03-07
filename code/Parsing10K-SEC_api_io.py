
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 20:24:09 2022

@author: cinde
"""
# %% https://sec-api.io/docs/sec-filings-item-extraction-api
# Very Important: Register and get an api code/key

!pip install sec_api
from sec_api import ExtractorApi
# %% Very important: Register and get an api key!!!

# extractorApi = ExtractorApi("Your-API-Code/Key")


# extractorApi = ExtractorApi("")
# %% Tesla 10-K filing
filing_url = "https://www.sec.gov/Archives/edgar/data/1318605/000156459021004599/tsla-10k_20201231.htm"

# %% get the standardized and cleaned text of section 1A "Risk Factors"
section_text = extractorApi.get_section(filing_url, "7", "text")

# %% get the original HTML of section 7 "Management’s Discussion and Analysis of Financial Condition and Results of Operations"
section_html = extractorApi.get_section(filing_url, "7", "html")

print(section_text)
print(section_html)
# %%
