import requests
import pandas as pd
import os

GOOGLE_API_KEY = "AIzaSyBA_P9fZ8prDUsRLN4WxcNfUpOwfp5PKk8"


def get_google_reviews():
    query = "New Deal Motors Waterloo Iowa"

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    res = requests.get(url, params={"query": query, "key": GOOGLE_API_KEY}).json()

    if "results" not in res or len(res["results"]) == 0:
        return []

    place_id = res["results"][0]["place_id"]

    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    details = requests.get(details_url, params={
        "place_id": place_id,
        "fields": "reviews",
        "key": GOOGLE_API_KEY
    }).json()

    if "result" not in details or "reviews" not in details["result"]:
        return []

    return [r["text"] for r in details["result"]["reviews"]]


def get_all_data():
    data = get_google_reviews()

    df = pd.DataFrame({"text": data})

    # optional safe save (only if folder exists)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/raw_data.csv", index=False)

    return df
