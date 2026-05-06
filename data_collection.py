import requests
import pandas as pd

GOOGLE_API_KEY = "AIzaSyBA_P9fZ8prDUsRLN4WxcNfUpOwfp5PKk8"

def get_reviews(keyword):
    """
    Robust Google Places data collector:
    - returns reviews if available
    - otherwise returns place metadata as fallback text
    """

    if not keyword:
        return pd.DataFrame({"text": []})

    search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    search_res = requests.get(search_url, params={
        "query": keyword,
        "key": GOOGLE_API_KEY
    }).json()

    results = search_res.get("results", [])

    print("\n GOOGLE RESULTS RAW OUTPUT:")
    print(search_res)

    if not results:
        print("No places found at all")
        return pd.DataFrame({"text": []})

    all_text = []

    print("\nPLACES FOUND:")
    print("-" * 50)

    for place in results:

        name = place.get("name", "Unknown")
        address = place.get("formatted_address", "No address")
        rating = place.get("rating", "No rating")
        place_id = place.get("place_id")

        print(f"\n {name}")
        print(f" {address}")
        print(f" Rating: {rating}")

        # STEP 1: TRY REVIEWS
 
        reviews_url = "https://maps.googleapis.com/maps/api/place/details/json"

        details = requests.get(reviews_url, params={
            "place_id": place_id,
            "fields": "name,rating,reviews",
            "key": GOOGLE_API_KEY
        }).json()

        reviews = details.get("result", {}).get("reviews", [])

        # CASE 1: REVIEWS EXIST
 
        if reviews:
            for r in reviews:
                text = r.get("text")
                if text:
                    all_text.append(text)

  
        # CASE 2: NO REVIEWS → USE METADATA

        else:
            fallback_text = f"{name} located at {address} has rating {rating}"
            all_text.append(fallback_text)

    # FINAL SAFETY CHECK
    if not all_text:
        all_text.append("No review data available from Google Places API")

    return pd.DataFrame({"text": all_text})
