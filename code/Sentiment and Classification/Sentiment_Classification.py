# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 23:33:15 2022

@author: cinde
"""
# %% 
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# %% With ProsusAI FinBert
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert",num_labels=3)

prosusai_nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# %% Analysis

sentences = ["there is a shortage of capital, and we need extra financing",  
             "growth is strong and we have plenty of liquidity", 
             "there are doubts about our finances", 
             "profits are flat"]

prosusai_results = prosusai_nlp(sentences)

# %% show results
print(prosusai_results)

# %% finbert-tone Does not work. finbert-pretrain works. HKUST Sentiment Analysis-Classification
finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-pretrain',num_labels=3)
tokenizer_hkust = BertTokenizer.from_pretrained('yiyanghkust/finbert-pretrain')
# %%
nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer_hkust)

sentences = ["there is a shortage of capital, and we need extra financing",  
             "growth is strong and we have plenty of liquidity", 
             "there are doubts about our finances", 
             "profits are flat"]
# %% 
results = nlp(sentences)
print(results)


# %% topic classification
zero_shot_classifier = pipeline('zero-shot-classification', model="roberta-large-mnli")
sequence = "A new moon has been discovered in Jupiter's orbit by Moscow University."
class_names = ["the world", "Russia", "business"]
zero_shot_classifier(sequence, class_names)