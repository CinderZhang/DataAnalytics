# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 23:33:15 2022

@author: cinde
"""

from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

sentences = ["there is a shortage of capital, and we need extra financing",  
             "growth is strong and we have plenty of liquidity", 
             "there are doubts about our finances", 
             "profits are flat"]
results = nlp(sentences)
print(results)

# %% topic classification
zero_shot_classifier = pipeline('zero-shot-classification', model="roberta-large-mnli")
sequence = "A new moon has been discovered in Jupiter's orbit by Moscow University."
class_names = ["the world", "Russia", "business"]
zero_shot_classifier(sequence, class_names)