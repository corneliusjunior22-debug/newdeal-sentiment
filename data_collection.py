import requests
import pandas as pd

GOOGLE_API_KEY = "AIzaSyBA_P9fZ8prDUsRLN4WxcNfUpOwfp5PKk8"


def get_reviews(keyword):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    res = requests.get(url, params={
        "query": keyword,
        "key": GOOGLE_API_KEY
    }).json()

    if "results" not in res or len(res["results"]) == 0:
        return pd.DataFrame({"text": []})

    place_id = res["results"][0]["place_id"]

    details_url = "https://maps.googleapis.com/maps/api/place/details/json"

    details = requests.get(details_url, params={
        "place_id": place_id,
        "fields": "reviews",
        "key": GOOGLE_API_KEY
    }).json()

    reviews = details.get("result", {}).get("reviews", [])

    texts = [r["text"] for r in reviews]

    return pd.DataFrame({"text": texts})
