import pandas as pd
from scipy.sparse import coo_matrix, save_npz, load_npz
from tqdm import tqdm
import json

CSV_FILE = "all_users_data.csv"
OUTPUT_MATRIX = "user_song_matrix.npz"
CHUNKSIZE = 100000  

def process_large_csv(file_path, chunksize):
    user_list, song_list, values = [], [], []
    user_map, song_map = {}, {}
    user_counter = 0
    song_counter = 0
    song_id_to_info = {}

    for chunk in tqdm(pd.read_csv(file_path, usecols=["user_id", "master_metadata_track_name", "master_metadata_album_artist_name", "ms_played", "skipped"], chunksize=chunksize)):
        for _, row in chunk.iterrows():
            user = row['user_id']
            skipped = row['skipped']
            song = row['master_metadata_track_name']
            artist = row['master_metadata_album_artist_name']
            play_time = row['ms_played']
            if skipped == True:
                continue
            if play_time < 3000:
                continue

            if pd.isna(song) or pd.isna(artist):  
                continue
            
            if user not in user_map:
                user_map[user] = user_counter
                user_counter += 1

            song_key = (song, artist)  

            if song_key not in song_map:
                song_map[song_key] = song_counter
                song_id_to_info[song_counter] = {"title": song, "artist": artist}
                song_counter += 1

            user_list.append(user_map[user])
            song_list.append(song_map[song_key])
            values.append(play_time)

    with open("song_id_to_info.json", "w") as f:
        json.dump(song_id_to_info, f)

    return user_list, song_list, values, user_counter, song_counter

user_indices, song_indices, values, num_users, num_songs = process_large_csv(CSV_FILE, CHUNKSIZE)

sparse_matrix = coo_matrix((values, (user_indices, song_indices)), shape=(num_users, num_songs))

save_npz(OUTPUT_MATRIX, sparse_matrix)
print(f"Sparse matrix saved as {OUTPUT_MATRIX} with shape {sparse_matrix.shape}")

# To reload the matrix later:
# sparse_matrix = load_npz(OUTPUT_MATRIX)
