import streamlit as st
import pandas as pd
import sys
import os

# FIX PATH (Streamlit safe)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)


# IMPORT MODULES (NO src/)

from data_collection import get_reviews
from preprocessing import clean_text
from feature_engineering import fit_transform
from train_model import train
from evaluate import evaluate

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()


# UI CONFIG

st.set_page_config(page_title="Brand Sentiment Analysis", layout="wide")
st.title("Google Reviews Sentiment Dashboard")



# SENTIMENT FUNCTION (NO FAKE LABELS)

def get_sentiment(text):
    score = sia.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    return "neutral"



# USER INPUT (KEYWORD SEARCH)

keyword = st.text_input("Enter Business / Brand Name (e.g. New Deal Motors Waterloo Iowa)")

if st.button("Analyze Reviews"):

    if not keyword:
        st.error("Please enter a search term.")
        st.stop()

    # STEP 1: GET GOOGLE REVIEWS
    df = get_reviews(keyword)

    if df is None or df.empty:
        st.error("No reviews found for this search term.")
        st.stop()

    # STEP 2: CLEAN TEXT
    df["clean"] = df["text"].fillna("").apply(clean_text)
    df = df[df["clean"].str.strip() != ""]

    if df.empty:
        st.error("No usable text after cleaning.")
        st.stop()

    # STEP 3: SENTIMENT LABELS (VADER)
    df["sentiment"] = df["clean"].apply(get_sentiment)

    # STEP 4: FEATURE ENGINEERING (TF-IDF)
    X = fit_transform(df["clean"])
    y = df["sentiment"]

    # STEP 5: TRAIN MODEL
    model = train(X, y)

    # STEP 6: PREDICTIONS
    df["prediction"] = model.predict(X)

   
    # DASHBOARD OUTPUT


    st.subheader("Review Data")
    st.dataframe(df)

    st.subheader("Sentiment Breakdown")
    st.bar_chart(df["sentiment"].value_counts())

    st.subheader("Model Predictions")
    st.bar_chart(df["prediction"].value_counts())

    # TREND ANALYSIS

    df["index"] = range(len(df))
    trend = df.groupby(["index", "sentiment"]).size().unstack().fillna(0)

    st.subheader("Sentiment Trend")
    st.line_chart(trend)

    # DOWNLOAD DATA

    st.download_button(
        "Download Results",
        df.to_csv(index=False),
        "sentiment_results.csv",
        "text/csv"
    )
