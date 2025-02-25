import os
import zipfile
import re

# Define paths
ZIP_FOLDER = "spotify_stream_data"  # Folder containing the ZIP files
OUTPUT_FOLDER = "spotifyDatas"  # Folder where all files will be extracted

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Process each ZIP file
for filename in os.listdir(ZIP_FOLDER):
    if filename.endswith(".zip"):
        zip_path = os.path.join(ZIP_FOLDER, filename)
        
        # Extract number from ZIP filename (e.g., "spotify12.zip" → "12")
        zip_number = re.search(r'\d+', filename)
        zip_number = zip_number.group() if zip_number else "unknown"

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for file in zip_ref.namelist():
                # Get just the filename, ignoring any directory structure inside the ZIP
                base_filename = os.path.basename(file)

                # Only extract files that start with "Streaming_History"
                if not base_filename.startswith("Streaming_History"):
                    continue  # Skip files that don't match

                file_name, file_ext = os.path.splitext(base_filename)
                
                # Append zip number to file name
                new_file_name = f"{file_name}_{zip_number}{file_ext}"
                extracted_path = os.path.join(OUTPUT_FOLDER, new_file_name)

                # Rename if file already exists to avoid overwriting
                base, ext = os.path.splitext(extracted_path)
                counter = 1
                while os.path.exists(extracted_path):
                    extracted_path = f"{base}_{counter}{ext}"
                    counter += 1

                # Extract file
                with zip_ref.open(file) as source, open(extracted_path, "wb") as target:
                    target.write(source.read())

print("All relevant files extracted successfully into:", OUTPUT_FOLDER)
