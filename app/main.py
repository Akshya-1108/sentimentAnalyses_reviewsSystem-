# app/main.py

#isort: off
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#isort: on
import streamlit as st
import pandas as pd
from model.roberta_model import predict_sentiment
from utils.visualization import plot_sentiment_by_rating



st.set_page_config(page_title="RoBERTa Review Analyzer", layout="wide")
st.title("📊 RoBERTa Review Sentiment Analyzer")

uploaded_file = st.file_uploader(
    "Upload a CSV with a 'review' column", type='csv')

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if 'review' not in df.columns:
        st.error("The CSV must contain a column named 'review'.")
    else:
        reviews = df['review'].dropna().astype(str).tolist()
        sentiments, score_df = predict_sentiment(reviews)

        df = df.loc[df['review'].notna()].reset_index(drop=True)
        df['sentiment'] = sentiments
        df = pd.concat([df, score_df], axis=1)

        st.subheader("📄 Sample Output")
        st.dataframe(df[['review', 'sentiment']].head())

        st.subheader("📈 Sentiment Distribution")
        st.bar_chart(df['sentiment'].value_counts())

        if 'rating' in df.columns:
            st.subheader("📊 Sentiment Score by Rating")
            fig = plot_sentiment_by_rating(df)
            st.pyplot(fig)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Annotated CSV", csv,
                           "sentiment_reviews.csv", "text/csv")
