import streamlit as st
import pandas as pd
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src.data_collection import get_all_data
from src.preprocessing import clean_text
from src.feature_engineering import fit_transform
from src.train_model import train
from src.evaluate import evaluate

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

st.set_page_config(page_title="New Deal Motors Sentiment", layout="wide")
st.title("New Deal Motors Sentiment Dashboard (Waterloo, IA)")


# REAL SENTIMENT (NO FAKE LABELS)
def get_sentiment(text):
    score = sia.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    return "neutral"


if st.button("Load Latest Reviews"):

    # STEP 1: GET DATA
    df = get_all_data()

    if df is None or df.empty:
        st.error("No reviews found.")
        st.stop()

    # STEP 2: CLEAN TEXT
    df["clean"] = df["text"].fillna("").apply(clean_text)
    df = df[df["clean"].str.strip() != ""]

    if df.empty:
        st.error("No usable text after cleaning.")
        st.stop()

    # STEP 3: REAL SENTIMENT LABELS (VADER)
    df["sentiment"] = df["clean"].apply(get_sentiment)

    # STEP 4: FEATURES
    X = fit_transform(df["clean"])
    y = df["sentiment"]

    # STEP 5: TRAIN MODEL
    model = train(X, y)

    # STEP 6: PREDICTIONS
    df["prediction"] = model.predict(X)

    #UI
    st.subheader("Data Preview")
    st.dataframe(df)

    st.subheader("Sentiment Breakdown")
    st.bar_chart(df["sentiment"].value_counts())

    st.subheader("Model Predictions")
    st.bar_chart(df["prediction"].value_counts())

    # Trend chart
    df["index"] = range(len(df))
    trend = df.groupby(["index", "sentiment"]).size().unstack().fillna(0)

    st.subheader("Sentiment Trend")
    st.line_chart(trend)

    st.download_button(
        "Download Data",
        df.to_csv(index=False),
        "sentiment_data.csv",
        "text/csv"
    )
