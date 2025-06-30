import streamlit as st
import pandas as pd
import os

from apify_utils import run_trending_scraper


st.set_page_config(page_title="TikTok Trending Discovery", layout="wide")

st.title("🎵 TikTok Trending Discovery Tool")
st.markdown("This tool pulls the top 100 trending TikTok sounds via Apify.")

# Run button
if st.button("Fetch Trending Songs"):
    with st.spinner("Fetching data from Apify..."):
        st.write("API key loaded:", os.getenv("APIFY_API_KEY"))
        df = run_trending_scraper()
        if df is not None and not df.empty:
            st.success(f"Fetched {len(df)} songs!")
            st.dataframe(df)

            # Download buttons
            csv = df.to_csv(index=False).encode("utf-8")
            json = df.to_json(orient="records")
            st.download_button("Download CSV", csv, "trending_songs.csv", "text/csv")
            st.download_button("Download JSON", json, "trending_songs.json", "application/json")
        else:
            st.error("No data was returned from Apify.")

