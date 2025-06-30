import requests
import time

RAPIDAPI_KEY = "813ec90f04msh60b85bd19042914p1d5c47jsnc3f5ecaea33a"  # Replace with st.secrets later

API_URL = "https://shazam.p.rapidapi.com/search"

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "shazam.p.rapidapi.com"
}

def shazam_lookup(title: str, artist: str) -> dict:
    """Query Shazam for a given song title and artist. Returns metadata."""
    query = f"{title} {artist}"
    params = {"term": query, "locale": "en-US", "offset": "0", "limit": "1"}

    try:
        res = requests.get(API_URL, headers=HEADERS, params=params, timeout=10)
        data = res.json()

        hits = data.get("tracks", {}).get("hits", [])
        if not hits:
            return {}

        track = hits[0]["track"]
        return {
            "Shazam Title": track.get("title"),
            "Shazam Artist": track.get("subtitle"),
            "Label": track.get("sections", [{}])[0].get("metadata", [{}])[0].get("text", ""),
        }
    except Exception as e:
        print("Shazam lookup failed:", e)
        return {}

