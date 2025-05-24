# model/roberta_model.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

labels = ['negative', 'neutral', 'positive']


def predict_sentiment(texts):
    encoded_input = tokenizer(
        texts, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        output = model(**encoded_input)
        scores = torch.nn.functional.softmax(output.logits, dim=1)
        predictions = torch.argmax(scores, dim=1)
    sentiment_labels = [labels[p.item()] for p in predictions]
    score_df = pd.DataFrame(scores.numpy(), columns=['neg', 'neu', 'pos'])
    return sentiment_labels, score_df
