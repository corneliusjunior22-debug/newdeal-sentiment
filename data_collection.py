import requests
import pandas as pd

GOOGLE_API_KEY = "AIzaSyBA_P9fZ8prDUsRLN4WxcNfUpOwfp5PKk8"


# GET GOOGLE REVIEWS BY KEYWORD

def get_reviews(keyword):
    """
    Fetch Google Places reviews based on a search keyword.
    Example: "New Deal Motors Waterloo Iowa"
    """

    if not keyword:
        return pd.DataFrame({"text": []})

    try:
        # STEP 1: SEARCH PLACE
        search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

        search_res = requests.get(search_url, params={
            "query": keyword,
            "key": GOOGLE_API_KEY
        }).json()

        results = search_res.get("results", [])

        if not results:
            return pd.DataFrame({"text": []})

        place_id = results[0].get("place_id")

        if not place_id:
            return pd.DataFrame({"text": []})

        # STEP 2: GET REVIEWS
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"

        details_res = requests.get(details_url, params={
            "place_id": place_id,
            "fields": "reviews",
            "key": GOOGLE_API_KEY
        }).json()

        reviews = details_res.get("result", {}).get("reviews", [])

        if not reviews:
            return pd.DataFrame({"text": []})

        # STEP 3: EXTRACT TEXT
        texts = [r.get("text", "") for r in reviews if r.get("text")]

        return pd.DataFrame({"text": texts})

    except Exception as e:
        print("Error fetching reviews:", e)
        return pd.DataFrame({"text": []})
