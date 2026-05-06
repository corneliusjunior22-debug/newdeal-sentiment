import streamlit as st
import pandas as pd

from data_collection import get_reviews
from preprocessing import clean_text
from feature_engineering import fit_transform
from train_model import train
from evaluate import evaluate

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

st.set_page_config(page_title="Sentiment Dashboard", layout="wide")
st.title("Google Reviews Sentiment Analysis")


# -----------------------------
# SENTIMENT FUNCTION
# -----------------------------
def get_sentiment(text):
    score = sia.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    return "neutral"


# -----------------------------
# USER INPUT
# -----------------------------
keyword = st.text_input("Enter business name or keyword")

if st.button("Analyze"):

    df = get_reviews(keyword)

    if df.empty:
        st.error("No data found")
        st.stop()

    # CLEAN TEXT
    df["clean"] = df["text"].fillna("").apply(clean_text)

    # REMOVE EMPTY ROWS
    df = df[df["clean"].str.strip() != ""]

    if df.empty:
        st.error("No usable text after cleaning")
        st.stop()

    # SENTIMENT LABELS (VADER)
    df["sentiment"] = df["clean"].apply(get_sentiment)

    # FEATURES
    X = fit_transform(df["clean"])
    y = df["sentiment"]

    # TRAIN MODEL
    model = train(X, y)

    # PREDICTIONS
    df["prediction"] = model.predict(X)

    # -----------------------------
    # UI OUTPUT
    # -----------------------------
    st.subheader("Data")
    st.dataframe(df)

    st.subheader("Sentiment Distribution")
    st.bar_chart(df["sentiment"].value_counts())

    st.subheader("Predictions")
    st.bar_chart(df["prediction"].value_counts())

    st.subheader("Trend")
    df["index"] = range(len(df))
    trend = df.groupby(["index", "sentiment"]).size().unstack().fillna(0)
    st.line_chart(trend)
