import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X)"
}

def get_spotify_label(song_title: str, artist_name: str) -> dict:
    query = f"{song_title} {artist_name}".replace(" ", "+")
    search_url = f"https://open.spotify.com/search/{query}/tracks"

    try:
        res = requests.get(search_url, headers=HEADERS)
        if res.status_code != 200:
            return {"error": f"Failed to load search page ({res.status_code})"}

        soup = BeautifulSoup(res.text, "html.parser")

        # Find the first track link
        match = re.search(r'"uri":"spotify:track:(.*?)"', res.text)
        if not match:
            return {"error": "Track ID not found in search results"}
        track_id = match.group(1)

        # Visit album page via track page
        track_url = f"https://open.spotify.com/track/{track_id}"
        res = requests.get(track_url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        album_match = re.search(r'"uri":"spotify:album:(.*?)"', res.text)
        if not album_match:
            return {"error": "Album ID not found"}
        album_id = album_match.group(1)

        # Now get album metadata
        album_url = f"https://open.spotify.com/album/{album_id}"
        res = requests.get(album_url, headers=HEADERS)
        if res.status_code != 200:
            return {"error": "Album page fetch failed"}

        label_match = re.search(r"℗[^<]+", res.text)
        label_text = label_match.group(0).strip() if label_match else "Unknown"

        return {
            "track": song_title,
            "artist": artist_name,
            "album": album_id,
            "label": label_text
        }

    except Exception as e:
        return {"error": str(e)}
