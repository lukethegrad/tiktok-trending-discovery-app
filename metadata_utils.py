import requests

SPOTIFY_API_URL = "https://spotify-label-api.fly.dev/spotify_label"

def get_spotify_label(title: str, artist: str) -> dict:
    """Query your deployed Spotify label scraper."""
    params = {"song": title, "artist": artist}

    try:
        res = requests.get(SPOTIFY_API_URL, params=params, timeout=15)
        data = res.json()
        return {
            "Spotify Title": data.get("track"),
            "Spotify Artist": data.get("artist"),
            "Album": data.get("album"),
            "Spotify Label": data.get("label")
        }
    except Exception as e:
        print("Spotify label lookup failed:", e)
        return {}
