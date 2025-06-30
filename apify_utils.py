import os
import requests
import time
import pandas as pd


APIFY_API_KEY = os.getenv("APIFY_API_KEY")
SCRAPER_ACTOR = "lexis-solutions~tiktok-trending-songs-scraper"


def run_trending_scraper():
    run_url = f"https://api.apify.com/v2/acts/{SCRAPER_ACTOR}/runs?token={APIFY_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    # You can customize input here later, e.g., {"maxItems": 100}
    payload = {}

    st.write("Sending POST request to Apify...")

    response = requests.post(run_url, headers=headers, json=payload)
    st.write(f"Apify POST status: {response.status_code}")

    if response.status_code != 201:
        st.error(f"Failed to start Apify actor. Status code: {response.status_code}")
        st.error(response.text)
        return None

    run_id = response.json()["data"]["id"]
    st.write(f"Apify run started: {run_id}")

    # 2. Poll for status
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}"
    for _ in range(30):
        time.sleep(5)
        status_res = requests.get(status_url)
        status_data = status_res.json()["data"]
        status = status_data["status"]
        st.write(f"Apify status: {status}")
        if status == "SUCCEEDED":
            break
    else:
        st.error("Apify run did not finish successfully.")
        return None

    # 3. Fetch dataset
    dataset_id = status_data.get("defaultDatasetId")
    st.write(f"Using dataset ID: {dataset_id}")
    if not dataset_id:
        st.error("No dataset ID found.")
        return None

    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?clean=true"
    data_res = requests.get(dataset_url)
    st.write(f"Dataset fetch status: {data_res.status_code}")

    if data_res.status_code != 200:
        st.error(f"Failed to fetch dataset: {data_res.status_code}")
        return None

    records = data_res.json()
    st.write(f"Number of records: {len(records)}")

    if not records:
        st.warning("Apify returned an empty dataset.")
        return None

    df = pd.DataFrame(records)
    return df
