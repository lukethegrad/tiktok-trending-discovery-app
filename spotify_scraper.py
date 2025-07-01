import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X)"
}

def scrape_spotify_label(song_title: str, artist_name: str) -> dict:
    try:
        print(f"[DEBUG] Starting label scrape for: {song_title} by {artist_name}")

        query = f"{song_title} {artist_name}".replace(" ", "+")
        search_url = f"https://open.spotify.com/search/{query}/tracks"
        print(f"[DEBUG] Search URL: {search_url}")

        res = requests.get(search_url, headers=HEADERS)
        print(f"[DEBUG] Search response status: {res.status_code}")
        if res.status_code != 200:
            return {"error": f"Failed to load search page (status {res.status_code})"}

        # Search for track ID
        match = re.search(r'"uri":"spotify:track:(.*?)"', res.text)
        if not match:
            print("[DEBUG] No track ID found in search results")
            return {"error": "Track ID not found in search results"}
        track_id = match.group(1)
        print(f"[DEBUG] Found track ID: {track_id}")

        # Get album page from track page
        track_url = f"https://open.spotify.com/track/{track_id}"
        print(f"[DEBUG] Track URL: {track_url}")
        res = requests.get(track_url, headers=HEADERS)
        print(f"[DEBUG] Track page status: {res.status_code}")
        if res.status_code != 200:
            return {"error": "Failed to load track page"}

        album_match = re.search(r'"uri":"spotify:album:(.*?)"', res.text)
        if not album_match:
            print("[DEBUG] Album ID not found on track page")
            return {"error": "Album ID not found"}
        album_id = album_match.group(1)
        print(f"[DEBUG] Found album ID: {album_id}")

        # Load album page
        album_url = f"https://open.spotify.com/album/{album_id}"
        print(f"[DEBUG] Album URL: {album_url}")
        res = requests.get(album_url, headers=HEADERS)
        print(f"[DEBUG] Album page status: {res.status_code}")
        if res.status_code != 200:
            return {"error": "Album page fetch failed"}

        label_match = re.search(r"℗[^<]+", res.text)
        label_text = label_match.group(0).strip() if label_match else "Unknown"
        print(f"[DEBUG] Extracted label: {label_text}")

        return {
            "track": song_title,
            "artist": artist_name,
            "album_id": album_id,
            "label": label_text
        }

    except Exception as e:
        print(f"[ERROR] Exception during scraping: {e}")
        return {"error": str(e)}
