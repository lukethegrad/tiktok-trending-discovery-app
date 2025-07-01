# app.py

from flask import Flask, request, jsonify
from spotify_scraper import scrape_spotify_label  # or get_spotify_label if you renamed it

app = Flask(__name__)

@app.route("/spotify_label", methods=["GET"])
def get_spotify_label():
    song = request.args.get("song")
    artist = request.args.get("artist")

    if not song or not artist:
        return jsonify({"error": "Missing 'song' or 'artist' query parameter"}), 400

    result = scrape_spotify_label(song, artist)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
