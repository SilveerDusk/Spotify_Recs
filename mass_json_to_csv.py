import os
import json
import pandas as pd
import re

# Define the folder containing extracted JSON files
DATA_FOLDER = "spotifyDatas"

# Initialize an empty list to store all records
all_data = []

# Process each JSON file in the folder
for filename in os.listdir(DATA_FOLDER):
    if filename.startswith("Streaming_History") and filename.endswith(".json"):
        file_path = os.path.join(DATA_FOLDER, filename)
        
        # Extract user_id from filename (e.g., "Streaming_History_Audio_12.json" → "12")
        user_id_match = re.search(r'_(\d+)\.json$', filename)
        user_id = user_id_match.group(1) if user_id_match else "unknown"

        # Load JSON data
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                
                # Add user_id to each record
                for record in data:
                    record["user_id"] = user_id
                    all_data.append(record)
            
            except json.JSONDecodeError:
                print(f"Skipping {filename} due to JSON decoding error.")

# Convert to DataFrame
df = pd.DataFrame(all_data)

# Save as CSV (optional)
df.to_csv("all_users_data.csv", index=False)

print("Data successfully loaded into DataFrame!")
