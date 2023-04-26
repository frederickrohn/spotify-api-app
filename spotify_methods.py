from dotenv import load_dotenv
import os
import json
import base64
from requests import post, get
import datetime

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#takes in nothing
#returns the access token needed for the Spotify API
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def _get_auth_header(token):
    return {"Authorization": "Bearer " + token}

#takes in a token and a name
#returns a dictionary that contains the artist information
def search_for_artist_by_name(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = _get_auth_header(token)

    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    #just to let you know it didn't work
    if len(json_result) == 0:
        print("No artist with that name exists!")
        return None
    
    return json_result[0]

#takes in a token and a artist's id
#returns a dictionary that contains the artist information
def search_for_artist_by_id(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = _get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

#takes in a token and artist's id
#returns a list of the songs and all information about each song (each song is a dictionary)
def get_top_ten_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = _get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

#takes in a token and artist's id
#doesn't return anything, just prints the top 10 song names and their popularities by the artist
def print_top_songs_today(token, artist_id):
    songs = get_top_ten_songs_by_artist(token, artist_id)
    print(datetime.date.today())
    
    for i in range(len(songs)):
        print(i + 1, songs[i]["name"], songs[i]["popularity"])


#takes in a token and an artist_id
#returns a list of strings of related genres to the artist
def get_related_genres(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = _get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["genres"]
    return json_result

#takes in a token and and artist_id
#returns a list of artists (and all their details)
def get_related_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    headers = _get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['artists']
    return json_result


def test():
    t = get_token()
    drake = search_for_artist_by_name(t, "drake")
    print(drake["name"], drake["id"])
    print(search_for_artist_by_id(t, drake["id"]))
    get_top_ten_songs_by_artist(t, drake["id"])
    
    #this prints related artists
    ra = get_related_artists(t, drake["id"])
    for item in ra:
        print(item["name"])

    print(get_related_genres(t, drake["id"]).keys())


test()
