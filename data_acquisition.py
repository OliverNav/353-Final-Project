#data_acquisition.py: scrapes API to generate csv with data
import time
import os
import requests
import numpy as np
import pandas as pd

BASE_URL = "https://api.mcsrranked.com"
OUTPUT_FILE = "mcsr_matches_dataset.csv"

#double check how long to sleep for
def fetch_match_details(match_id):
    url = f"{BASE_URL}/matches/{match_id}"
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("data", {})
        elif response.status_code == 429:
            print("limit reached, pausing for 45 seconds")
            time.sleep(45)
        else:
            return {}

#if i want more than 2000, make sure to change at the bottom as well
def collect_matches(target_match_count=2000):
    if os.path.exists(OUTPUT_FILE):
        existing_df = pd.read_csv(OUTPUT_FILE)
        collected_ids = set(existing_df["match_id"].tolist())
        records = existing_df.to_dict("records")
    else:
        collected_ids = set()
        records = []

    if not records:
        last_match_id = None
    else:
        last_match_id = records[-1]["match_id"]
    
    while len(records) < target_match_count:
        url = f"{BASE_URL}/matches"
        params = {"count": 100, "type": 2, "excludedecay": "true"}
        if last_match_id:
            params["before"] = last_match_id
            
        res = requests.get(url, params=params)
        if res.status_code != 200:
            time.sleep(10)
            continue
            
        batch = res.json().get("data", [])
        if not batch:
            print("No more matches available from API.")
            break
            
        last_match_id = batch[-1]["id"]

        for match in batch:
            m_id = match.get("id")
            if m_id in collected_ids:
                continue

            time.sleep(1.2)
            
            details = fetch_match_details(m_id)
            if not details:
                continue

            seed_info = details.get("seed")
            overworld_type = seed_info.get("overworld")
            if not overworld_type:
                continue

            is_forfeited = details.get("forfeited", False)
            result = details.get("result", {})
            winning_time_ms = result.get("time")

            changes = details.get("changes", [])
            elos = [c.get("eloRate") for c in changes if c.get("eloRate") is not None]
            if elos:
                avg_elo = np.mean(elos)
            else:
                avg_elo = np.nan

            records.append({
                "match_id": m_id,
                "overworld_seed": overworld_type.upper().replace("_", " "),
                "avg_elo": avg_elo,
                "is_forfeited": is_forfeited,
                "winning_time_sec": (winning_time_ms / 1000.0) if (winning_time_ms and not is_forfeited) else np.nan
            })
            collected_ids.add(m_id)

            #save every 50 records
            if len(records) % 50 == 0:
                pd.DataFrame(records).to_csv(OUTPUT_FILE, index=False)

            if len(records) >= target_match_count:
                break

    final_df = pd.DataFrame(records)
    final_df.to_csv(OUTPUT_FILE, index=False)

if __name__ == "__main__":
    collect_matches(2000)