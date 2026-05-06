import requests
import pandas as pd

GOOGLE_API_KEY = "AIzaSyBA_P9fZ8prDUsRLN4WxcNfUpOwfp5PKk8"

def get_reviews(keyword):
    """
    Fetch Google Places reviews for a keyword search
    """

    if not keyword:
        return pd.DataFrame({"text": []})

    # STEP 1: SEARCH PLACES
    search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    search_res = requests.get(search_url, params={
        "query": keyword,
        "key": GOOGLE_API_KEY
    }).json()

    results = search_res.get("results", [])

    if not results:
        print("No places found")
        return pd.DataFrame({"text": []})

    all_reviews = []

    print("\n GOOGLE SEARCH RESULTS:")
    print("-" * 50)

    # STEP 2: LOOP ALL MATCHED PLACES
    for place in results:

        name = place.get("name", "Unknown")
        address = place.get("formatted_address", "No address")
        place_id = place.get("place_id")

        print(f"\n {name}")
        print(f"   {address}")

        if not place_id:
            continue

        # STEP 3: GET PLACE DETAILS (REVIEWS)
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"

        details_res = requests.get(details_url, params={
            "place_id": place_id,
            "fields": "name,rating,reviews",
            "key": GOOGLE_API_KEY
        }).json()

        reviews = details_res.get("result", {}).get("reviews", [])

        # STEP 4: EXTRACT TEXT
        for r in reviews:
            text = r.get("text")
            if text:
                all_reviews.append(text)

    return pd.DataFrame({"text": all_reviews})
