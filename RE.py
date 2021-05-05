# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# WRDS.wharton.upenn.edu
# Python on WRDS: https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-python/
# Sample code: https://wrds-www.wharton.upenn.edu/pages/support/applications/python-replications/



# %%

import wrds
import numpy as np
import pandas as pd

import re

 
#%% Search a keyword in N-CSR file and save the text;
# filing full text: 
# https://www.sec.gov/Archives/edgar/data/918294/000120677421000348/0001206774-21-000348.txt
 
# 3 paragraphs. Use ''' to input multile lines;
lines = '''<P style="TEXT-ALIGN: left"><FONT size=2 face=Arial>The energy sector also featured several detractors from performance. Global exploration and production company </FONT><B><FONT size=2 face=Arial>Occidental Petroleum </FONT></B><FONT size=2 face=Arial>fell sharply in March as the company was forced to slash its spending projections in the wake of the Saudi-Russian oil market share battle, which sent crude prices lower. The stock finished the year as a significant absolute and relative detractor, and we trimmed most of our position in recognition of the changing risk profile of the investment brought on by the pandemic. </FONT><B><FONT size=2 face=Arial>ExxonMobil </FONT></B><FONT size=2 face=Arial>suffered from operational headwinds related to the coronavirus pandemic, which adversely impacted the company&#8217;s near-term earnings power. However, our underweight in the name benefited relative returns for the year.</FONT></P>
    <P style="TEXT-ALIGN: left"><FONT size=2 face=Arial>Elsewhere in the portfolio, shares of </FONT><B><FONT size=2 face=Arial>Tyson Foods </FONT></B><FONT size=2 face=Arial>declined early in the period due to input cost inflation and broader market uncertainty stemming from the coronavirus pandemic, which hampered exports to China and shifted demand to residential use from food services. Industry-wide price-fixing allegations also pressured shares of chicken companies during the period. We are optimistic that improving chicken fundamentals will drive the stock higher over the near term. Shares of </FONT><B><FONT size=2 face=Arial>Boeing </FONT></B><FONT size=2 face=Arial>suffered amid delays in the 737 MAX recertification process and pressure on air travel from coronavirus fears. While we continue to find Boeing shares attractive, we are cognizant of the uncertain near-term recovery path of global air travel post-pandemic and, therefore, largely kept our position flat in the name throughout the year.</FONT></P>
    <P style="TEXT-ALIGN: left"><FONT size=2 face=Arial>Some of the portfolio&#8217;s largest absolute contributors came from the information technology sector. Shares of </FONT><B><FONT size=2 face=Arial>Qualcomm </FONT></B><FONT size=2 face=Arial>rebounded from the first-quarter sell-off, rising considerably for the one-year period due to the company&#8217;s strong position in 5G cellular technology. During the period, the company was able to resolve all its remaining licensing disputes, thereby stabilizing that business and leaving investors to focus on its earnings growth runway as 5G devices proliferate. Shares of </FONT><B><FONT size=2 face=Arial>Microsoft </FONT></B><FONT size=2 face=Arial>rose as the company reported robust growth within its Intelligent Cloud segment. Investors appeared to prioritize Microsoft&#8217;s solid fundamentals, defensible business model, and attractive growth potential. We trimmed both positions throughout the year on strength.</FONT></P>
'''
keyword = "optimistic|energy"

 

sentences = re.split('(\<P|\<P\>)', lines)

 

#sentences_terminated = [a + b for a,b in zip(sentences[0::2], sentences[1::2])]

 

# print(sentences_terminated)

 
str=""
for line in sentences:
    if re.search(keyword,line):
        print(line)
        str=str+line
# You can remove all the html marks as you wish from the str variable;


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

# %% regular expression sample

# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Regular expressions
# %% [markdown]
# A *regular expression* (also called a *regex*, or *RE*) is a sequence of characters that defines a pattern to be searched for within a longer piece of text.
# 
# They are not specific to Python, and can be found in various languages and tools. (Google Sheets has several regex functions, for example.)
# %% [markdown]
# What follows is an introduction to regular expressions. It is not a complete guide; regexes can be quite complicated, and there are many details that I'm glossing over. Generally, these details tend not to be important if your goal is collecting and cleaning data.
# %% [markdown]
# That said, I highly recommend reading both
# 
# * [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html); and
# * the `re` [documentation](https://docs.python.org/3/library/re.html)
# 
# at some point to really dive into the details of regexes. There are also many online resources and books available about regexes. One great tool for practicing writing your own regexes is [RegExr](https://regexr.com/).
# %% [markdown]
# Suppose we have data like this, and want to extract email addresses.

# %%
data = '''

Associate Professor - WCOB
479-575-7094
xili@uark.edu

Assistant Professor - WCOB
479-575-4505
kuanliu@uark.edu

Professor
Department Chair
479-575-6095
pliu@uark.edu


Assistant Professor - WCOB
479-575-4505
al045@uark.edu'''


# %%
data


# %%
print(data)

# %% [markdown]
# We can extract what we want by identifying a regex pattern that describes what an email address looks like and applying the pattern to our text.

# %%
import re


# %%
emails=re.findall(r'\w+@\w+\.edu', data)

# %% [markdown]
# Or we might want to find the phone numbers:

# %%
phones=re.findall(r'\d{3}\-\d{3}\-\d{4}', data)


# %%
phones2 = re.findall(r'[\d\-]{12}', data)

ap=re.findall(r"[^\r\n]*?Assistant[^.]*[\b\r\n]+",data)  

# %% [markdown]
# ## Meta characters
# 
# The basic building blocks of a regular expression are *meta characters*, which each have a special meaning within the context of an RE.
# 
# These characters are:
# 
# `. ^ $ * + ? { } [ ] \ | ( )`
# 
# 
# 
# 
# %% [markdown]
# Anything that isn't a meta character will just match itself.
# 
# For example, the pattern `python` will match only the string `python`. (It would also match `pythons` or `pythonista` unless we're careful to tell it otherwise.)
# %% [markdown]
# ## Character classes
# 
# Square brackets are used to define a *character class*, or a pattern of characters to match.
# 
# * `[abc$`] will match any single `a`, `b`, `c`, or `$` character. Note that the special meaning of meta characters does not apply within a character class, so the `$` means simply that character.
# 
# * `[a-z]` matches any single English lowercase letter. The `-` character specifies a range in this context.
# %% [markdown]
# `re.search(pattern, string, flags)` uses a regex `pattern` to find the first match in `string`. Additional options may be set with the `flags` variable.

# %%
s = "Here is a string of text. It's not that interesting, is it?"


# %%
findit = re.search(r'[a-z]', s)


# %%
# Include both lower and uppercase letters
findit=re.search(r'[A-z]', s)


# %%
# Another way, using a RE flag
re.search(r'[a-z]', s, re.IGNORECASE)

# %% [markdown]
# Inside a character class, `^` causes *negation*.

# %%
re.search(r'[^A-z]', s)

# %% [markdown]
# ### Quantifiers
# 
# A character class can be repeated using *quantifiers*.
# 
# 
# | Quantifier | Matches preceding token: |
# | --- | --- |
# |`*` | zero or more times |
# |`+` | one or more times |
# |`?` | zero or one times |
# |`{n}` | exactly *n* times |
# |`{min,}` | *min* or more times |
# |`{min,max}` | at least *min* times, but not more than *max* times |

# %%
re.search(r'[a-z]{4}', s)


# %%
re.search(r'[A-Z][a-z]+', s)

# %% [markdown]
# Notice that matching is *greedy*: the regex engine will match the **longest possible string** it can find.

# %%
re.search(r'[A-Z][a-z]*', s)

# %% [markdown]
# The `?` character can also be used after a `*` or `+` to limit the scope of the search, making it *lazy* rather than greedy.

# %%
re.search(r'[A-Z][a-z]*?', s)

# %% [markdown]
# `re.search` finds up to *one* match and returns a match object. `re.findall` finds all matches and returns a (possibly empty) list.

# %%
re.findall(r'[A-Z][a-z]+', s)


# %%
re.findall(r'[A-Z][A-Z]+', s)

# %% [markdown]
# Various character classes are pre-defined as special characters:
# 
# * `.` matches any character, except for a newline character. Adding the `re.DOTALL` flag causes the newline character to be included as well.
# * `\w` is any "word" character. In ASCII text, this is equivalent to `[a-zA-Z0-9_]`.
# * `\d` is any digit, equivalent to `[0-9]`.
# * `\s` is any whitespace character, equivalent to `[ \t\n\r\f\v]`. Note that `\n` is the *newline* character (generally corresponding to `<enter>` or `<return>`) and `\t` is a `<tab>` character. I've never come across `\f` or `\v` in about 25 years of working with regular expressions.
# * `\b` is a *word boundary*, or the place where a word begins or ends, where "word" means any alphanumeric sequence.
# 
# The special characters `\W`, `\D`, `\S`, and `\B` are the negated versions of the corresponding lowercase special character. So, for example, `\W` matches any non-word character.

# %%
re.search(r'\W+', s)


# %%
print(re.findall(r'\b\w+\b', s))

# %% [markdown]
# The `\` character is the escape character. If you want to refer to a character that has a special meaning, first escape it with `\`.
# 
# For example, the `.` has a special meaning, so if we want to find a period in text, we use `\.`.

# %% greedy by default
re.search(r'\w+\.', s)


# %% add ? to make it lazy,i.e. capture as little as possible
re.findall(r'\w+[\.\?]', s)


# %%
print(data)


# %%
prof=re.findall(r'(.+)\n(.*Professor)', data)

# %% [markdown]
# The other meta characters are:
# 
# * `$` matches at the end of a line, defined either as the end of the string, or any location followed by a newline character.
# * `^` matches the beginning of lines. This will only match at the beginning of the string, unless the `MULTILINE` flag is used, in which case this also matches immediately after each newline within the string.
# * `|` is the "or" operator. If *A* and *B* are regular expressions, `A|B` will match any string that matches either *A* or *B*. Importantly, `|` has very low precedence, so `Fama|French` will match either "Fama" or "French", not "Fam" followed either an "a" or an "F", followed by "rench".
# %% [markdown]
# ## Capturing groups
# 
# We are often interested in using information to perform a match, but only want to extract a piece of the match. This is where *capturing groups* come in.

# %%
totc = '''It was the best of times, it was the worst of times,
it was the age of wisdom, it was the age of foolishness,
it was the epoch of belief, it was the epoch of incredulity,
it was the season of Light, it was the season of Darkness,
it was the spring of hope, it was the winter of despair,
we had everything before us, we had nothing before us...'''


# %%
itwas=re.findall(r'it was the (.+? of .+?\b)', totc, re.IGNORECASE)

# %% [markdown]
# <img src="http://clipart-library.com/images/pT5rBGGac.gif" alt="Question" style="width: 50px; float: left; margin-right: 20px;"/>
# 
# 
# These alternatives are not quite right. Can you see what is causing each to go wrong, and how my code above solves the problem?

# %%
re.findall(r'it was the (.+ of .+)', totc, re.IGNORECASE)


# %%
re.findall(r'it was the (.+? of .+?)', totc, re.IGNORECASE)

# %% Sentence with certain words [coronavirus|liquidity] i.e. coronavirus or liquidity
statement='''However, a shift occurred early in 2020, as the coronavirus spread across the globe.As equity and credit markets entered free-fall in March, a flight to quality ensued. The Fed, as well as other global central banks and governments, enacted historic monetary and fiscal assistance 
and quantitative easing programs. These efforts helped to provide liquidity within credit markets and ease investor anxiety brought on by widespread lockdowns and their dampening effects on economic activity. 
As part of these measures, the Fed cut the target overnight lending rate to near zero. This led to falling interest rates across much of the Treasury curve, boosting returns for Treasuries. 
In addition, the Fed purchase of corporate credit worked to support risk asset prices. Generally, investment-grade corporate debt outperformed like-duration Treasuries over the period. 
High-yield debt lagged the broader market, due in part to the high concentration of energy issuers within the universe. Energy companies lagged the broader market for much of the year.'''


kw=re.findall("[^.]* [coronavirus|liquidity] [^.]*\.",statement)

# %% [markdown]
# ### Accessing groups

# %%
ptrn = r'(\d{1,2})-(\d{1,2})-(\d{4})'

m = re.search(ptrn, '01-20-2020')


# %%
m


# %%
m.group(1)


# %%
m.group(2)


# %%
m.group(3)


# %%
# group(0) is always the complete matched pattern, regardless of what is captured
m.group(0)


# %%
m.group(3,2)


# %%
m.groups()

# %% [markdown]
# What happens when there is no match?

# %%
m2 = re.search(ptrn, "This date doesn't match the pattern: 2020-02-15")


# %%
m2


# %%
print(m2)


# %%
type(m2)


# %%
m2.group(0)

# %% [markdown]
# ### Compiling regex patterns
# 
# Regex patterns can be *compiled* in python, creating a regex pattern object. I tend not to bother with this very often in my own code, but you'll often see it used.

# %%
p = re.compile(ptrn)


# %%
p


# %%
p.search('12-15-2019').group(3)

# %% [markdown]
# # Using regular expressions
# %% [markdown]
# ## Simple web scraping
# %% [markdown]
# Suppose we need a dictionary of state names and their abbreviations to do some data cleaning.
# 
# [Here's a list](https://abbreviations.yourdictionary.com/articles/state-abbrev.html) of state names and their corresponding abbreviations. We can quickly read that in to get what we want with a regex.
# 
# <img src="https://kelley.iu.edu/nstoffma/da/statenames_webpage.png?1" alt="Webpage" style="width: 1000px;border: 1px solid;"/>

# %%
import requests

url = 'https://abbreviations.yourdictionary.com/articles/state-abbrev.html'
html = requests.get(url).text


# %%
html[:50]

# %% [markdown]
# The HTML source of this page looks like this:
# 
# ![Source](https://kelley.iu.edu/nstoffma/da/statenames_source.png)

# %%
states = re.findall(r'<li><p>(.+?) - ([A-Z]{2})', html)
states[:10]


# %%
states = dict(states)


# %%
states['Florida']

# %% [markdown]
# ## A *Project Gutenberg* book
# %% [markdown]
# Next, let's download Adam Smith's *The Wealth of Nations* from [Project Gutenberg](http://www.gutenberg.org/).
# 
# We can see links to various formats of the book [here](http://www.gutenberg.org/ebooks/3300). We'll take the one that's stored as a text file.

# %%
text = requests.get('http://www.gutenberg.org/ebooks/3300.txt.utf-8').text

print('{:.2} MB'.format(len(text)/1e6))


# %%
text[:500]

# %% [markdown]
# ### Special character encoding
# 
# We can see right away that there appear to be some strange characters in the document: There are `\r\n` characters sprinkled throughout, and the documents starts with `\ufeff`.
# 
# We saw above that the character `\n` represents a *newline* character. On Windows machines, pressing `<enter>` actually [generates two characters](https://en.wikipedia.org/wiki/Newline#Representation) representing *carriage return* and *linefeed*, so if text was created on Windows newlines are represented by `\r\n`.
# 
# The other character is basically garabage:
# 
# https://stackoverflow.com/questions/17912307/u-ufeff-in-python-string
# %% [markdown]
# If we print the text rather than looking at the raw string, these special characters will be interpreted and used to affect the displayed output:

# %%
print(text[:1000])

# %% [markdown]
# ### The `.DOTALL` flag
# 
# The `.` meta characer matches anything except a newline character, unless the “dot-all” option is used.
# 
# Compare these two results:

# %%
re.findall('.{15}[Bb]aker.{15} ', text)


# %%
re.findall('.{15}[Bb]aker.{15} ', text, re.DOTALL)

# %% [markdown]
# How might we remove the header and footer from the text?

# %%
text.find('*** END OF THIS')


# %%
print(text[2257400:2257700])


# %%
re.search(r'\*\*\* START OF .*? \*\*\*(.+?)\*\*\* END OF', text)


# %%
re.search(r'\*\*\* START OF .*? \*\*\*(.+?)\*\*\* END OF', text, re.DOTALL)


# %%
book = re.search(r'\*\*\* START OF .*? \*\*\*(.+?)\*\*\* END OF', text, re.DOTALL).group(1)


# %%
print(book[:250])


# %%
print(book[-250:])

# %% [markdown]
# Let's download another book to see if the pattern of text around the beginning and end of the book content is the same.

# %%
text2 = requests.get('http://www.gutenberg.org/ebooks/1342.txt.utf-8').text


# %%
book2 = re.search(r'\*\*\* START OF .*? \*\*\*(.+?)\*\*\* END OF', text2, re.DOTALL).group(1)


# %%
book2[:500]


# %%
book2[-500:]


# %%
ptrn = r'\r\nProduced by .+?\r\n(.+?)\r\nEnd of the Project Gutenberg EBook'

book2 = re.search(ptrn, text2, re.DOTALL).group(1)


# %%
book2[:500]


# %%
book2[-500:]

# %% [markdown]
# Here's an alternative approach using the `.span()` method of the RE object.

# %%
re.search(r'\n\r\nProduced by .+?\r\n', text2).span()


# %%
re.search(r'\r\nEnd of the Project Gutenberg EBook', text2).span()


# %%
_, start = re.search(r'\r\nProduced by .+?\r\n', text2).span()

end, _ = re.search(r'\r\nEnd of the Project Gutenberg EBook', text2).span()


# %%
start, end


# %%
book2 = text2[start:end]

# %% [markdown]
# Let's put this together in a function that also cleans up the text a bit.

# %%
def get_book(bookid):
    req = requests.get(f'http://www.gutenberg.org/ebooks/{bookid}.txt.utf-8')
    if req.ok:
        text = req.text
        
        _, start = re.search(r'\r\nProduced by .+?\r\n', text).span()
        end, _ = re.search(r'\r\nEnd of the Project Gutenberg EBook', text).span()

        book = text[start:end].replace('\r\n', '\n').strip()

        header = text[:start]

        title = re.search(r'Title: (.+)', header).group(1)

        author = re.search(r'Author: (.+)', header)
        if author:
            author = author.group(1)

        return (title, author, book)
    else:
        print(f'Problem downloading book {bookid}')


# %%
book = get_book(1342)


# %%
print(book[2][:500])


# %%
book = get_book(10)
print(book[2][:500])

# %% [markdown]
# <img src="http://clipart-library.com/images/pT5rBGGac.gif" alt="Question" style="width: 50px; float: left; margin-right: 20px;"/>
# 
# Uh-oh, that isn't working. It looks like our search for "Produced by" is failing. As an exercise, can you figure out where this is going wrong? How might you think about fixing it?

# %%
book = get_book(98)
print(book[2][:500])

# %% [markdown]
# Next, let's look at [the list](http://www.gutenberg.org/browse/scores/top) of most-downloaded books.

# %%
books = requests.get('http://www.gutenberg.org/browse/scores/top').text


# %%
m = re.search(r'<ol>(.+?)</ol>', books, re.DOTALL)

top100 = re.findall(r'/ebooks/(\d+)">(.+?) \((\d+)\)</a>', m.group(1))
top100[:10]

# %% [markdown]
# <img src="http://clipart-library.com/images/pT5rBGGac.gif" alt="Question" style="width: 50px; float: left; margin-right: 20px;"/>
# 
# Since `re.search` finds the first instance of a match, this code downloads the *first* list (between the `<ol>` and `</ol>` tags) on the page, so we're downloading the top-downloaded books from yesterday. Can you think of a way to get the records from one of the *other* lists on the page, say the top-100 in the last 30 days?

# %%
top100 = {int(id):(title,int(count)) for id,title,count in top100}


# %%
top100[1342]


# %%
top100[10]


# %%
[title for title,count in top100.values()][:25]


# %%
[title.split(' by ') for title,count in top100.values()][:10]


# %%
[re.search(r'(.+?) by (.+)$', title).groups() for title,count in top100.values()][:25]


# %%
[re.search(r'(.+?) by (.+)$', title) for title,count in top100.values()][:25]


# %%
[re.search(r'(.+?)(?: by (.+))?$', title).groups() for title,count in top100.values()][:25]

# %% [markdown]
# ## A *Wall Street Journal* article

# %%
with open('WSJ_article.txt', 'r', encoding='utf-8') as inf:
    wsj = inf.read()


# %%
print(wsj[:2500])


# %%
# find a quotation

re.findall(r'".+?"', wsj)

# %% [markdown]
# Why doesn't that work? Look closesly at the quotation marks in the article.

# %%
# a regular quotation mark
ord('"')


# %%
# quote symbols used in the article
ord('“'), ord('”')


# %%
re.findall(r'“.+?”', wsj)


# %%
re.findall(r'[A-Z\.]{3,}', wsj)


# %%
re.findall(r'\w+ly\b', wsj)


# %%
re.findall(r'\w+est\b', wsj)

# %% [markdown]
# ### Working with punctuation

# %%
re.escape('!')


# %%
re.escape('.')


# %%
import string
string.punctuation


# %%
''.join([re.escape(p) for p in string.punctuation])


# %%
ptrn = '[' + ''.join([re.escape(p) for p in string.punctuation]) + ']'
ptrn


# %%
set(re.findall(ptrn, wsj))


# %%
import calendar

print([calendar.month_name[k] for k in range(1,13)])


# %%
mos = '|'.join([calendar.month_name[k][:3] for k in range(1,13)])
mos


# %%
mo_ptrn = '(?:' + mos + ')\. \d+'
mo_ptrn


# %%
re.findall(mo_ptrn, wsj)

# %% [markdown]
# <img src="http://clipart-library.com/images/pT5rBGGac.gif" alt="Question" style="width: 50px; float: left; margin-right: 20px;"/>
# 
# As the code below shows, if we don't group the month names, the regex fails. Do you see why? Try experimenting with a simple example on [RegExr](http://regexr.com/4igtc).
# 
# Hint: remember that `|` has very low precedence in the regex context.

# %%
re.findall(mos + r'\. \d+', wsj)

# %% [markdown]
# ### Finding people

# %%
re.findall(r'Mrs?\. (\w+)', wsj)


# %%
re.findall(r'\b(\w+) \([RD]\.,', wsj)


# %%
from collections import Counter

names = Counter()
for name in re.findall(r'Mrs?\. (\w+)', wsj) + re.findall(r'\b(\w+) \([RD]\.,', wsj):
    names[name] += 1

names


# %%
names *2


# %%
re.findall(r'\(([RD])\., (.+?)\)', wsj)

# %% [markdown]
# ## Getting Fidelity fund tickers
# %% [markdown]
# https://www.fidelity.com/mutual-funds/fidelity-funds/overview

# %%
url = 'https://www.fidelity.com/mutual-funds/fidelity-funds/overview'

html = requests.get(url).text


# %%
funds = re.findall(r'/(\d+)">([A-Z]+)</a>', html)
funds[:10]


# %%
len(funds)


# %%
len(set(funds))

# %% [markdown]
# By looking at the HTML source, we can come up with a more complicated regex that gets the fund name as well.

# %%
funds = re.findall(r'<br />\s+(.+?)\(.+?/(\d+)">([A-Z]+)</a>', html)
funds[:10]


# %%
[(name.replace('<sup>®</sup>', ''), int(id), ticker) for (name, id, ticker) in funds]

# %% [markdown]
# For cleaning text it's often easiest to create a function that does the various steps. Building such functions is often an iterative process, requiring some trial-and-error.

# %%
def cleaner(s):
    s = s.replace(u'\xa0', ' ')   # non-breaking space
    s = s.replace('&amp;', '&')
    s = s.replace('<sup>®</sup>', '')
    s = s.replace('<font color="#FF6800">NEW</font>', '')
    return s


# %%
cleaner('Fidelity<sup>®</sup> Export &amp; Multinational Fund ')


# %%
[cleaner(name) for (name, _, _) in funds]    


# %%
def cleaner(s):
    s = s.replace(u'\xa0', ' ')
    s = s.replace('&amp;', '&')
    s = s.replace('<sup>®</sup>', '')
    s = s.replace('<font color="#FF6800">NEW</font>', '')
    return s.strip()
    
[cleaner(name) for (name, _, _) in funds]    


# %%
def cleaner(s):
    s = s.replace(u'\xa0', ' ').replace('&amp;', '&')
    s = re.sub(r'<.+?>.+?</.+?>', ' ', s)
    s = re.sub(r' +', ' ', s)
    return s.strip()
    
[cleaner(name) for (name, _, _) in funds]    


# %%
[(cleaner(name), int(id), ticker) for (name, id, ticker) in funds]

# %% [markdown]
# ## *New York Times* headlines

# %%
yr, mo, dt = 2020, 7, 15

url = f'https://www.nytimes.com/issue/todayspaper/{yr}/{mo:02}/{dt:02}/todays-new-york-times'


# %%
print(url)


# %%
req = requests.get(url)


# %%
req.text


# %%
articles = re.findall(r'href="([\w/-]+?\.html)"><h2.*?>(.+?)</h2>', req.text)
articles[:5]


# %%
len(articles)


# %%
for url, headline in articles[:5]:
    print(re.search(r'^([\d/]+/)([\w/]+)/(.+?\.html)', url).groups())


# %%
from collections import defaultdict

nyt = defaultdict(list)

for url, headline in articles:
    pubdt, topic, file = re.search(r'^([\d/]+/)([\w/]+)/(.+?\.html)', url).groups()
    nyt[topic].append((pubdt, headline, file))


# %%
nyt['us/politics']


# %%
nyt.keys()

# %% [markdown]
# Hm, why is there a topic “18”?

# %%
articles[-2]


# %%
nyt = defaultdict(list)

for url, headline in articles:
    pubdt, topic, file = re.search(r'^([\d/]+/)([\w/\-]+)/(.+?\.html)', url).groups()
    nyt[topic].append((pubdt, headline, file))


# %%
nyt.keys()


# %%
for topic in nyt.keys():
    print(f'{topic.upper()}\n' + '-'*len(topic))
    for dt, headline, file in nyt[topic]:
        url = 'https://www.nytimes.com' + dt + topic + '/' + file
        print(url)
        # Do something here like:
        # html = requests.get(url).text
    print('\n')

# %% [markdown]
# ## Extra credit: Regex golf
# 
# [Peter Norvig](http://norvig.com/) is probably one of the most respected computer scientists today. His web site is a treasure trove of interesting things, including the [sort-of famous](http://norvig.com/Gettysburg/making.html) PowerPoint slides for the Gettysburg Address.
# 
# He's written an interesting set of code using regular expressions that is also closely related to machine learning in Python. It's a great example of very clean code. There's [a video](https://www.oreilly.com/learning/regex-golf-with-peter-norvig) of him explaining his approach. (If you watch the video, scroll down a bit and the video will move to a corner of the screen and you can see the code at the same time.

