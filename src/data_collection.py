import requests
import tweepy
import pandas as pd

GOOGLE_API_KEY = "AIzaSyBA_P9fZ8prDUsRLN4WxcNfUpOwfp5PKk8"
TWITTER_BEARER = "YOUR_TWITTER_BEARER_TOKEN"


# GOOGLE REVIEWS (PRIMARY SOURCE)
def get_google_reviews():
    query = "New Deal Motors Waterloo Iowa"

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    res = requests.get(url, params={"query": query, "key": GOOGLE_API_KEY}).json()

    place_id = res["results"][0]["place_id"]

    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    reviews = requests.get(details_url, params={
        "place_id": place_id,
        "fields": "reviews",
        "key": GOOGLE_API_KEY
    }).json()

    return [r["text"] for r in reviews["result"].get("reviews", [])]


# TWITTER DATA (SECONDARY SOURCE)
def get_tweets():
    client = tweepy.Client(bearer_token=TWITTER_BEARER)

    tweets = client.search_recent_tweets(
        query="New Deal Motors Waterloo",
        max_results=50
    )

    return [t.text for t in tweets.data] if tweets.data else []


# COMBINE DATA SOURCES
def get_all_data():
    data = []
    data += get_google_reviews()
    data += get_tweets()

    df = pd.DataFrame({"text": data})
    df.to_csv("data/raw_data.csv", index=False)

    return df
