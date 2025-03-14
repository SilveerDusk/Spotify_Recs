import json
import numpy as np
from scipy.sparse import load_npz
from collections import defaultdict

matrix = load_npz("user_song_matrix.npz")

print("Matrix shape:", matrix.shape)
print("Number of non-zero entries:", matrix.nnz)
print("Density:", matrix.nnz / (matrix.shape[0] * matrix.shape[1]))

import matplotlib.pyplot as plt



#print(matrix)
array_matrix = matrix.toarray()
with open("matrix_output.txt", "w") as f:
    for row in array_matrix:
        f.write(" ".join(map(str, row)) + "\n")


song_play_counts = np.array(matrix.sum(axis=0)).flatten()


with open("song_id_to_info.json", "r") as f:
    song_id_to_info = json.load(f)

def query_top_artists(n):

    artist_play_counts = defaultdict(int)

    for song_id, info in song_id_to_info.items():
        artist = info["artist"]
        artist_play_counts[artist] += song_play_counts[int(song_id)]

    top_artists = sorted(artist_play_counts.items(), key=lambda x: x[1], reverse=True)

    print("Top Played Artists:")
    for i, (artist, total_playtime) in enumerate(top_artists[:n], 1):
        print(f"{i}. {artist} - {total_playtime * 0.001} secs played")

def query_most_active_users(n):
    user_play_counts = np.array(matrix.sum(axis=1)).flatten()
    top_user_indices = np.argsort(user_play_counts)[::-1]

    print("Top Active Users:")
    for i, user_id in enumerate(top_user_indices[:n]):
        print(f"User {user_id}: {user_play_counts[user_id]} ms played")


def query_user_top_artists(user_id, n=10):
    """Query the top N most played artists for a specific user."""


    user_id = int(user_id)  
    if user_id >= matrix.shape[0]:
        print("Invalid user ID: out of range.")
        return
    
    user_play_counts = np.array(matrix.getrow(user_id).todense()).flatten()


    artist_play_counts = defaultdict(int)

    for song_id, playtime in enumerate(user_play_counts):
        if playtime > 0:  
            artist = song_id_to_info[str(song_id)]["artist"]
            artist_play_counts[artist] += playtime

    top_artists = sorted(artist_play_counts.items(), key=lambda x: x[1], reverse=True)

    print(f"Top {n} Artists for User {user_id}:")
    for i, (artist, total_playtime) in enumerate(top_artists[:n], 1):
        print(f"{i}. {artist} - {total_playtime * 0.001:.2f} secs played")

def top_songs_over_all_users(n=10):
    song_play_counts = np.array(matrix.sum(axis=0)).flatten()  
    top_song_indices = np.argsort(song_play_counts)[::-1]  


    top_songs = [(song_id_to_info[str(idx)]["title"], song_id_to_info[str(idx)]["artist"]) for idx in top_song_indices[:n]]

    print("Top Played Songs:")
    for i, (title, artist) in enumerate(top_songs, 1):
        print(f"{i}. {title} by {artist}")

def list_users_most_played_artist():
    """List each user's most played artist with playtime."""
    user_artist_counts = defaultdict(lambda: defaultdict(int))

    # Map users to their artists and playtime
    for user, song, playtime in zip(matrix.row, matrix.col, matrix.data):
        artist = song_id_to_info[str(song)]["artist"]
        user_artist_counts[user][artist] += playtime

    print("User's Most Played Artists:")
    for user, artist_dict in user_artist_counts.items():
        most_played_artist = max(artist_dict.items(), key=lambda x: x[1])
        artist, playtime = most_played_artist
        print(f"User {user}: {artist} - {playtime * 0.001:.2f} secs played")




if __name__ == "__main__":
    query_top_artists(10)
    query_most_active_users(39)
    query_user_top_artists(22)
    top_songs_over_all_users()
    #most_skipped_songs(100)
    list_users_most_played_artist()
