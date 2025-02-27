import os
import json
import pandas as pd
import re

DATA_FOLDER = "spotifyDatas"
OUTPUT_CSV = "all_users_data.csv"

all_data = []

for filename in os.listdir(DATA_FOLDER):
    if filename.startswith("Streaming_History") and filename.endswith(".json"):
        file_path = os.path.join(DATA_FOLDER, filename)

        user_id_match = re.search(r'_user(\d+)', filename)
        user_id = user_id_match.group(1) if user_id_match else "unknown"

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)

                for record in data:
                    record["user_id"] = user_id 
                    all_data.append(record)

            except json.JSONDecodeError:
                print(f"Skipping {filename} due to JSON decoding error.")

df = pd.DataFrame(all_data)

df.to_csv(OUTPUT_CSV, index=False)

print(f"Data successfully saved to {OUTPUT_CSV}!")
