import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import spotify_methods as sm
import actual_use as au

load_dotenv()

# Set up your Spotify API credentials
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://localhost:3000'

# Set up the scope required for playlist modification
scope = 'playlist-modify-private'

# Create an instance of the spotipy SpotifyOAuth object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

def create_playlist(artists, playlist_name):
    # Create a new playlist
    playlist = sp.user_playlist_create(sp.me()['id'], playlist_name, public=False)

    # Iterate over the artists in the dictionary
    for key, value in artists.items():

        artist_id = key

        # Get the top track for the artist
        if len(sp.artist_top_tracks(artist_id)['tracks']) == 0:
            continue
        
        top_track = sp.artist_top_tracks(artist_id)['tracks'][0]

        # Add the top track to the playlist
        sp.playlist_add_items(playlist['id'], [top_track['uri']])

    return playlist

def create_playlist_with_artist_choices():
    artist_name = input("Which artist do you want? ")
    t = sm.get_token()
    all_artists = au.find_related_arists_with_layers(t, sm.search_for_artist_by_name(t, artist_name)['id'], 2)
    sorted = au.filter_artist_dictionary(all_artists)
    playlist_name = input("What do you want your playlist to be called? ")
    new_playlist = create_playlist(sorted, playlist_name)
    print('Playlist link:', new_playlist['external_urls']['spotify'])

create_playlist_with_artist_choices()

