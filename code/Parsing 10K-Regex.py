# %% [markdown]
# # <span style="color:navy"> Intro
# 
# 
# In this notebook we will apply REGEX & BeautifulSoup to find useful financial information in 10-Ks. In particular, we will extract text from Items 1A, 7, and 7A of 10-K.

# %% [markdown]
# # <span style="color:navy"> STEP 1 : Import Libraries
# 
# Note that, we will need parser for BeautifulSoup, there are many parsers, we will be using 'lxml' which can be pre-installed as follows & it help BeatifulSoup read HTML, XML documents:
# 
# !pip install lxml

# %%
# Import requests to retrive Web Urls example HTML. TXT 
import requests

# Import BeautifulSoup
from bs4 import BeautifulSoup

# import re module for REGEXes
import re

# import pandas
import pandas as pd

# %% [markdown]
# # <span style="color:navy"> STEP 2 : Get Apple's [AAPL] 2018 10-K 
# 
# Though we are using AAPL as example 10-K here, the pipeline being built is generic & can be used for other companies 10-K
#  
# [SEC Website URL for 10-K (TEXT version)](https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/0000320193-18-000145.txt)
# 
# [SEC Website URL for 10-K (HTML version)](https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/a10-k20189292018.htm)
# It will be good to view/study along in html format to see how the below code would apply.
# 
# All the documents can be easily ssearched via CIK or company details via [SEC's search tool](https://www.sec.gov/cgi-bin/browse-edgar?CIK=0000320193&owner=exclude&action=getcompany&Find=Search)

# %%
# Get the HTML data from the 2018 10-K from Apple
r = requests.get('https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/0000320193-18-000145.txt')
raw_10k = r.text

# %% [markdown]
# If we print the `raw_10k` string we will see that it has many sections. In the code below, we print part of the `raw_10k` string:

# %%
print(raw_10k[0:1300])

# %% [markdown]
# # <span style="color:navy"> STEP 3 : Apply REGEXes to find 10-K Section from the document
# 
# For our purposes, we are only interested in the sections that contain the 10-K information. All the sections, including the 10-K are contained within the `<DOCUMENT>` and `</DOCUMENT>` tags. Each section within the document tags is clearly marked by a `<TYPE>` tag followed by the name of the section.

# %%
# Regex to find <DOCUMENT> tags
doc_start_pattern = re.compile(r'<DOCUMENT>')
doc_end_pattern = re.compile(r'</DOCUMENT>')
# Regex to find <TYPE> tag prceeding any characters, terminating at new line
type_pattern = re.compile(r'<TYPE>[^\n]+')

# %% [markdown]
# Define Span Indices using REGEXes
# 
# Now, that we have the regexes defined, we will use the `.finditer()` method to match the regexes in the `raw_10k`. In the code below, we will create 3 lists:
# 
# 1. A list that holds the `.end()` index of each match of `doc_start_pattern`
# 
# 2. A list that holds the `.start()` index of each match of `doc_end_pattern`
# 
# 3. A list that holds the name of section from each match of `type_pattern`

# %%
# Create 3 lists with the span indices for each regex

### There are many <Document> Tags in this text file, each as specific exhibit like 10-K, EX-10.17 etc
### First filter will give us document tag start <end> and document tag end's <start> 
### We will use this to later grab content in between these tags
doc_start_is = [x.end() for x in doc_start_pattern.finditer(raw_10k)]
doc_end_is = [x.start() for x in doc_end_pattern.finditer(raw_10k)]

### Type filter is interesting, it looks for <TYPE> with Not flag as new line, ie terminare there, with + sign
### to look for any char afterwards until new line \n. This will give us <TYPE> followed Section Name like '10-K'
### Once we have have this, it returns String Array, below line will with find content after <TYPE> ie, '10-K' 
### as section names
doc_types = [x[len('<TYPE>'):] for x in type_pattern.findall(raw_10k)]

# %% [markdown]
# Create a Dictionary for the 10-K
# 
# In the code below, we will create a dictionary which has the key `10-K` and as value the contents of the `10-K` section found above. To do this, we will create a loop, to go through all the sections found above, and if the section type is `10-K` then save it to the dictionary. Use the indices in  `doc_start_is` and `doc_end_is`to slice the `raw_10k` file.

# %%
document = {}

# Create a loop to go through each section type and save only the 10-K section in the dictionary
for doc_type, doc_start, doc_end in zip(doc_types, doc_start_is, doc_end_is):
    if doc_type == '10-K':
        document[doc_type] = raw_10k[doc_start:doc_end]

# %%
# display excerpt the document
document['10-K'][0:500]

# %% [markdown]
# # <span style="color:navy"> STEP 3 : Apply REGEXes to find Item 1A, 7, and 7A under 10-K Section 
# 
# The items in this `document` can be found in four different patterns. For example Item 1A can be found in either of the following patterns:
# 
# 1. `>Item 1A`
# 
# 2. `>Item&#160;1A` 
# 
# 3. `>Item&nbsp;1A`
# 
# 4. `ITEM 1A` 
# 
# In the code below we will write a single regular expression that can match all four patterns for Items 1A, 7, and 7A. Then use the `.finditer()` method to match the regex to `document['10-K']`.
# 
# Note that Item 1B & Item 8 are added to find out end of section Item 1A & Item 7A subsequently.

# %%
# Write the regex
regex = re.compile(r'(>Item(\s|&#160;|&nbsp;)(1A|1B|7A|7|8)\.{0,1})|(ITEM\s(1A|1B|7A|7|8))')

# Use finditer to math the regex
matches = regex.finditer(document['10-K'])

# Write a for loop to print the matches
for match in matches:
    print(match)

# %% [markdown]
# Notice that each item is matched twice. This is because each item appears first in the index and then in the corresponding section. We will now have to remove the matches that correspond to the index. We will do this using Pandas in the next section.

# %% [markdown]
# In the code below we will create a pandas dataframe with the following column names: `'item','start','end'`. In the `item` column save the `match.group()` in lower case letters, in the ` start` column save the `match.start()`, and in the `end` column save the ``match.end()`. 

# %%
# Matches
matches = regex.finditer(document['10-K'])

# Create the dataframe
test_df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])

test_df.columns = ['item', 'start', 'end']
test_df['item'] = test_df.item.str.lower()

# Display the dataframe
test_df.head()

# %% [markdown]
# Eliminate Unnecessary Characters
# 
# As we can see, our dataframe, in particular the `item` column, contains some unnecessary characters such as `>` and periods `.`. In some cases, we will also get unicode characters such as `&#160;` and `&nbsp;`. In the code below, we will use the Pandas dataframe method `.replace()` with the keyword `regex=True` to replace all whitespaces, the above mentioned unicode characters, the `>` character, and the periods from our dataframe. We want to do this because we want to use the `item` column as our dataframe index later on.

# %%
# Get rid of unnesesary charcters from the dataframe
test_df.replace('&#160;',' ',regex=True,inplace=True)
test_df.replace('&nbsp;',' ',regex=True,inplace=True)
test_df.replace(' ','',regex=True,inplace=True)
test_df.replace('\.','',regex=True,inplace=True)
test_df.replace('>','',regex=True,inplace=True)

# display the dataframe
test_df.head()

# %% [markdown]
# Remove Duplicates
# 
# Now that we have removed all unnecessary characters form our dataframe, we can go ahead and remove the Item matches that correspond to the index. In the code below we will use the Pandas dataframe `.drop_duplicates()` method to only keep the last Item matches in the dataframe and drop the rest. Just as precaution ensure that the `start` column is sorted in ascending order before dropping the duplicates.

# %%
# Drop duplicates
pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['item'], keep='last')

# Display the dataframe
pos_dat

# %% [markdown]
# Set Item to Index
# 
# In the code below use the Pandas dataframe `.set_index()` method to set the `item`  column as the index of our dataframe.

# %%
# Set item as the dataframe index
pos_dat.set_index('item', inplace=True)

# display the dataframe
pos_dat

# %% [markdown]
# <b> Get The Financial Information From Each Item </b>
# 
# The above dataframe contains the starting and end index of each match for Items 1A, 7, and 7A. In the code below, we will save all the text from the starting index of `item1a` till the starting index of `item1b` into a variable called `item_1a_raw`. Similarly, save all the text from the starting index of `item7` till the starting index of `item7a` into a variable called `item_7_raw`. Finally,  save all the text from the starting index of `item7a` till the starting of `item8` into a variable called `item_7a_raw`. We can accomplish all of this by making the correct slices of `document['10-K']`.

# %%
# Get Item 1a
item_1a_raw = document['10-K'][pos_dat['start'].loc['item1a']:pos_dat['start'].loc['item1b']]

# Get Item 7
item_7_raw = document['10-K'][pos_dat['start'].loc['item7']:pos_dat['start'].loc['item7a']]

# Get Item 7a
item_7a_raw = document['10-K'][pos_dat['start'].loc['item7a']:pos_dat['start'].loc['item8']]

# %% [markdown]
# Now that we have each item saved into a separate variable we can view them separately. For illustration purposes we will display Item 1a, but the other items will look similar.

# %%
item_1a_raw[0:1000]

# %% [markdown]
# We can see that the items looks pretty messy, they contain HTML tags, Unicode characters, etc... Before we can do a proper Natural Language Processing in these items we need to clean them up. This means we need to remove all HTML Tags, unicode characters, etc... In principle we could do this using regex substitutions as we learned previously, but his can be rather difficult. Luckily, packages already exist that can do all the cleaning for us, such as **Beautifulsoup**, let's make use of this to refine the extracted text.

# %% [markdown]
# # <span style="color:navy"> STEP 4 : Apply BeautifulSoup to refine the content

# %%
### First convert the raw text we have to exrtacted to BeautifulSoup object 
item_1a_content = BeautifulSoup(item_1a_raw, 'lxml')

# %%
### By just applying .pretiffy() we see that raw text start to look oragnized, as BeautifulSoup
### apply indentation according to the HTML Tag tree structure
print(item_1a_content.prettify()[0:1000])

# %%
### Our goal is though to remove html tags and see the content
### Method get_text() is what we need, \n\n is optional, I just added this to read text 
### more cleanly, it's basically new line character between sections. 
print(item_1a_content.get_text("\n\n"))

# %% [markdown]
# # <span style="color:navy"> Summary...

# %% [markdown]
# As we have seen that simply applying REGEX & BeautifulSoup combination we can form a very powerful combination extracting/scarpping content from any web-content very easily. Having said this, not all 10-Ks are well crafted HTML, TEXT formats, example older 10-Ks, hence there may be adjustments needed to adopt to the circumstances.


