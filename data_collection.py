import requests
import pandas as pd

GOOGLE_API_KEY = "AIzaSyBA_P9fZ8prDUsRLN4WxcNfUpOwfp5PKk8"

def get_reviews(keyword):

    if not keyword:
        return pd.DataFrame({"text": []})

    # -----------------------------
    # STEP 1: SEARCH PLACES
    # -----------------------------
    search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    search_res = requests.get(search_url, params={
        "query": keyword,
        "key": GOOGLE_API_KEY
    }).json()

    print("\nRAW RESPONSE:")
    print(search_res)

    print("\nSTATUS:", search_res.get("status"))

    results = search_res.get("results", [])

    if not results:
        print("No places found at all")
        return pd.DataFrame({"text": []})

    all_text = []

    print("\nPLACES FOUND:")
    print("-" * 50)

    # -----------------------------
    # STEP 2: LOOP RESULTS
    # -----------------------------
    for place in results:

        name = place.get("name", "Unknown")
        address = place.get("formatted_address", "No address")
        rating = place.get("rating", "No rating")
        place_id = place.get("place_id")

        print(f"\n{name}")
        print(f"{address}")
        print(f"Rating: {rating}")

        # -----------------------------
        # STEP 3: GET REVIEWS
        # -----------------------------
        reviews_url = "https://maps.googleapis.com/maps/api/place/details/json"

        details = requests.get(reviews_url, params={
            "place_id": place_id,
            "fields": "name,rating,reviews",
            "key": GOOGLE_API_KEY
        }).json()

        reviews = details.get("result", {}).get("reviews", [])

        # -----------------------------
        # CASE 1: REVIEWS FOUND
        # -----------------------------
        if reviews:
            for r in reviews:
                text = r.get("text")
                if text:
                    all_text.append(text)

        # -----------------------------
        # CASE 2: NO REVIEWS → FALLBACK
        # -----------------------------
        else:
            fallback_text = f"{name} located at {address} has rating {rating}"
            all_text.append(fallback_text)

    # -----------------------------
    # FINAL CHECK
    # -----------------------------
    if not all_text:
        all_text.append("No review data available from Google API")

    return pd.DataFrame({"text": all_text})
