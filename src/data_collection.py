import requests
import pandas as pd

GOOGLE_API_KEY = "AIzaSyBA_P9fZ8prDUsRLN4WxcNfUpOwfp5PKk8"


# GOOGLE REVIEWS
def get_google_reviews():
    query = "New Deal Motors Waterloo Iowa"

    # Step 1: Find place_id
    search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    res = requests.get(
        search_url,
        params={"query": query, "key": GOOGLE_API_KEY}
    ).json()

    # Safety check (prevents crash)
    if "results" not in res or len(res["results"]) == 0:
        print("No place found for query")
        return []

    place_id = res["results"][0]["place_id"]

    # Get reviews
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    details = requests.get(
        details_url,
        params={
            "place_id": place_id,
            "fields": "reviews",
            "key": GOOGLE_API_KEY
        }
    ).json()

    # Safety check
    if "result" not in details or "reviews" not in details["result"]:
        print("No reviews found")
        return []

    return [r["text"] for r in details["result"]["reviews"]]


# MAIN DATA FUNCTION
def get_all_data():
    data = get_google_reviews()

    df = pd.DataFrame({"text": data})

    # Save for model training
    df.to_csv("data/raw_data.csv", index=False)

    return df
