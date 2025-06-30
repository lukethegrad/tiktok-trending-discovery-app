import pandas as pd

def process_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    # Keep only relevant columns
    df = df[["title", "authorName", "soundId"]].copy()

    # Clean column names
    df.rename(columns={
        "title": "Title",
        "authorName": "Artist",
        "soundId": "Sound ID"
    }, inplace=True)

    # Construct TikTok URL
    df["TikTok Sound URL"] = df["Sound ID"].apply(
        lambda sid: f"https://www.tiktok.com/music/original-sound-{sid}" if pd.notna(sid) else None
    )

    # Drop rows with missing title or sound ID
    df.dropna(subset=["Title", "Sound ID"], inplace=True)

    # Remove duplicates
    df.drop_duplicates(subset=["Title", "Artist", "Sound ID"], inplace=True)

    # Reorder columns
    df = df[["Artist", "Title", "Sound ID", "TikTok Sound URL"]]

    return df.reset_index(drop=True)
