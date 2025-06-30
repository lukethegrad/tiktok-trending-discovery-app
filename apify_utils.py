import os
import requests
import time
import pandas as pd


APIFY_API_KEY = os.getenv("APIFY_API_KEY")
SCRAPER_ACTOR = "lexis-solutions~tiktok-trending-songs-scraper"


def run_trending_scraper():
    # 1. Trigger the actor
    run_url = f"https://api.apify.com/v2/acts/{SCRAPER_ACTOR}/runs?token={APIFY_API_KEY}"
    response = requests.post(run_url, json={})
    if response.status_code != 201:
        return None
    run_id = response.json()["data"]["id"]

    # 2. Poll for status
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}"
    for _ in range(30):
        time.sleep(5)
        status_res = requests.get(status_url)
        status = status_res.json()["data"]["status"]
        if status == "SUCCEEDED":
            break
    else:
        return None

    # 3. Fetch dataset
    dataset_id = status_res.json()["data"]["defaultDatasetId"]
    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?clean=true"
    data_res = requests.get(dataset_url)
    if data_res.status_code != 200:
        return None

    # 4. Parse to DataFrame
    records = data_res.json()
    df = pd.DataFrame(records)
    return df

