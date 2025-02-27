import os
import zipfile
import re
from collections import defaultdict

ZIP_FOLDER = "spotify_stream_data"  
OUTPUT_FOLDER = "spotifyDatas"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

zip_files = sorted(os.listdir(ZIP_FOLDER), key=lambda f: int(re.search(r'\d+', f).group()) if re.search(r'\d+', f) else float('inf'))

for filename in zip_files:
    if filename.endswith(".zip"):
        zip_path = os.path.join(ZIP_FOLDER, filename)

        # Extract user ID from ZIP filename (e.g., "spotify10.zip" → "10")
        user_id_match = re.search(r'\d+', filename)
        user_id = user_id_match.group() if user_id_match else "unknown"

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            file_count = defaultdict(int) 

            for file in zip_ref.namelist():
                base_filename = os.path.basename(file)

                if not base_filename.startswith("Streaming_History"):
                    continue

                file_count[base_filename] += 1
                internal_number = f"_{file_count[base_filename]}" if file_count[base_filename] > 1 else ""

                file_name, file_ext = os.path.splitext(base_filename)
                new_file_name = f"{file_name}_user{user_id}{internal_number}{file_ext}"
                extracted_path = os.path.join(OUTPUT_FOLDER, new_file_name)

                base, ext = os.path.splitext(extracted_path)
                counter = 1
                while os.path.exists(extracted_path):
                    extracted_path = f"{base}_v{counter}{ext}"  
                    counter += 1

                with zip_ref.open(file) as source, open(extracted_path, "wb") as target:
                    target.write(source.read())

print("All relevant files extracted successfully into:", OUTPUT_FOLDER)
