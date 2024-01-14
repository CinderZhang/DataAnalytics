# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 12:18:05 2022

@author: xz035
"""
import pandas as pd

from sec_api import ExtractorApi
# %% Very important: Register and get an api key!!!

extractorApi = ExtractorApi("API KEY")

# %% define the list of the filings
url = "C:\\Users\\xz035\\OneDrive - University of Arkansas\\Teaching\\University of Arkansas\\Financial Data Analytics I\\Spring2022\\TSLA_10K_url.xlsx"
print(url)

# %% read the list into a pandas dataframe
df = pd.read_excel(url)

for ind in df.index:
    weburl = df['url'][ind]
    print(weburl)
    #print(df['Company'][ind], df['url'][ind])
        
    # %% get the standardized and cleaned text of section 1A "Risk Factors"
    section_text = extractorApi.get_section(weburl, "7", "text")
    
    # %% get the original HTML of section 7 "Management’s Discussion and Analysis of Financial Condition and Results of Operations"
    #section_html = extractorApi.get_section(filing_url, "7", "html")
    print(df['Company'][ind])
    print(df['Year'][ind])
    print(section_text)
    # Save the sections into your hard drive.
    