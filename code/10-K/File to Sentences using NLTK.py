# %% Text to Sentences using NLTK
''' NLTK text to sentences'''
def txt2sentence(txt):
    '''file to sentence using NLTK'''
    import nltk
    nltk.download('punkt')
    from nltk.tokenize import sent_tokenize
    sentences = sent_tokenize(txt)
    df=pd.DataFrame(sentences)
    return df


    


# %% load packages
import nltk
''' if needed, download punkt'''
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import os
import pandas as pd



# %% Set up working folder and test its existence
# For better examples: https://www3.ntu.edu.sg/home/ehchua/programming/webprogramming/Python_FileText.html

folder='w:\\Finance\\Zhang\\Data_Analytics_I\\10K'
exist=os.path.exists(folder)
print(exist)
print(folder)

# %% Load the text file to a string variable
file=open(folder+"\\TSLA_10k_item7.txt",encoding="latin-1")
text=file.read()

print(text[0:500])

# %% Tokenize 
df_sentence = txt2sentence(text)

df_sentence.to_csv(folder+"\\tsla7a_processed.csv")



# %%
