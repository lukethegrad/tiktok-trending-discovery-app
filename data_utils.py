import pandas as pd
import streamlit as st

def process_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    # Show actual columns so we can debug
    st.write("Raw DataFrame columns:", list(df.columns))

    # Try to find matching columns (case-insensitive fallback)
    col_map = {}
    for col in df.columns:
        c = col.lower()
        if "title" in c:
            col_map["title"] = col
        elif "author" in c:
            col_map["authorName"] = col
        elif "soundid" in c or "sound_id" in c:
            col_map["soundId"] = col

    if not all(key in col_map for key in ["title", "authorName", "soundId"]):
        st.error("Required fields not found in the Apify dataset.")
        return pd.DataFrame()

    # Extract and clean
    df = df[[col_map["title"], col_map["authorName"], col_map["soundId"]]].copy()
    df.columns = ["Title", "Artist", "Sound ID"]

    df["TikTok Sound URL"] = df["Sound ID"].apply(
        lambda sid: f"https://www.tiktok.com/music/original-sound-{sid}" if pd.notna(sid) else None
    )

    df.dropna(subset=["Title", "Sound ID"], inplace=True)
    df.drop_duplicates(subset=["Title", "Artist", "Sound ID"], inplace=True)

    return df.reset_index(drop=True)
