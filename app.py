import streamlit as st
import pandas as pd

from src.data_collection import get_all_data
from src.preprocessing import clean_text
from src.feature_engineering import vectorizer
from src.train_model import train

st.title("New Deal Motors Sentiment Dashboard (Waterloo, IA)")

if st.button("Load Latest Reviews + Tweets"):
    df = get_all_data()

    df["clean"] = df["text"].apply(clean_text)

    # DEMO LABELS (replace later with real labeled dataset)
    y = ["positive"] * len(df)

    X = vectorizer.fit_transform(df["clean"])

    model = train(X, y)

    df["sentiment"] = model.predict(X)

    st.subheader("Data Preview")
    st.write(df)

    # SENTIMENT DISTRIBUTION
    st.subheader("Sentiment Breakdown")
    st.bar_chart(df["sentiment"].value_counts())

    # TREND GRAPH
    df["index"] = range(len(df))
    trend = df.groupby(["index", "sentiment"]).size().unstack().fillna(0)
    st.subheader("Sentiment Trend")
    st.line_chart(trend)
