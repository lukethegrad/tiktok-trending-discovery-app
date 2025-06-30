import streamlit as st
import pandas as pd
import os
import time

from apify_utils import run_trending_scraper
from data_utils import process_raw_data
from metadata_utils import shazam_lookup

st.set_page_config(page_title="TikTok Trending Discovery", layout="wide")

st.title("🎵 TikTok Trending Discovery Tool")
st.markdown("This tool pulls the top 100 trending TikTok sounds via Apify.")

# Helper to enrich each song with Shazam metadata
def enrich_with_metadata(df):
    enriched_rows = []
    for _, row in df.iterrows():
        meta = shazam_lookup(row["Title"], row["Artist"])
        enriched_rows.append({
            **row,
            **meta
        })
        time.sleep(0.75)  # Prevent rate-limiting on free RapidAPI plan
    return pd.DataFrame(enriched_rows)

# Main button
if st.button("Fetch Trending Songs"):
    with st.spinner("Fetching data from Apify..."):
        df = run_trending_scraper()
        if df is not None and not df.empty:
            clean_df = process_raw_data(df)
            st.success(f"Fetched {len(clean_df)} clean songs!")

            with st.spinner("Enriching with Shazam metadata..."):
                enriched_df = enrich_with_metadata(clean_df)
                st.dataframe(enriched_df)

            # Optional: Add download after enrichment is stable
            # csv = enriched_df.to_csv(index=False).encode("utf-8")
            # json = enriched_df.to_json(orient="records")
            # st.download_button("Download CSV", csv, "enriched_songs.csv", "text/csv")
            # st.download_button("Download JSON", json, "enriched_songs.json", "application/json")
        else:
            st.error("No data was returned from Apify.")
