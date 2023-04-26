# Credits: https://www.youtube.com/watch?v=WAmEZBEeNmg

#installing env and requests
# pip3 install python-dotenv
#pip3 install requests
#what do these do?

from dotenv import load_dotenv
import os
import json
import base64
from requests import post, get
import datetime

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#This tests that the env loading works, it does
#print("client id and secret: ", client_id, client_secret)

#this gives you the access token
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


def test_get_token():
    token = get_token()
    print("test token: ", token)
    return

#testing the get_token funciton
#test_get_token()

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with that name exists!")
        return None
    return json_result[0]
    
def test_search_for_artist():
    result = search_for_artist(get_token(), "Travis Scott")

    print(result["name"])


#test_search_for_artist()

#Takes in the result returned by search_for_artist and returns id
def get_artist_id(artist):
    return artist["id"]

def get_artist_popularity(artist):
    return artist['popularity']


def test_get_artist_id():
    artist = search_for_artist(get_token(), "Travis Scott")
    print(get_artist_id(artist))

#test_get_artist_id()

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def test_get_songs():
    token = get_token()
    travis_scott = search_for_artist(token, "Travis Scott")
    travis_scott_id = get_artist_id(travis_scott)

    songs = get_songs_by_artist(token, travis_scott_id)
    #print(songs[0])
    print(datetime.date.today())
    
    for i in range(len(songs)):
        print(i + 1, songs[i]["name"], songs[i]["popularity"])

#test_get_songs()

def get_related_genres(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["genres"]
    return json_result

def get_related_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_song_features(token, song_id):
    url = f"https://api.spotify.com/v1/audio-features/{song_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_azelrm():
    token = get_token()
    azel_rm = search_for_artist(token, "azel rm")
    azel_rm_id = get_artist_id(azel_rm)

    print("Azel's id: ", azel_rm_id)

    songs = get_songs_by_artist(token, azel_rm_id)
    #print(songs[0])
    print(datetime.date.today())
    print("Top 10")
    
    for i in range(len(songs)):
        print(i + 1, songs[i]["name"], songs[i]["popularity"])
    
    #print("hurt me again")
    #print(songs[3])

    print("related genres:")
    print(get_related_genres(token, azel_rm_id))

    print("related artists:")
    print(get_related_artists(token, azel_rm_id))

    print("top song:")
    top_song_id = songs[0]["id"]
    song_features = get_song_features(token, top_song_id)

    for key, value in song_features.items(): 
        print(f"{key}: {value}")



#get_azelrm()

def get_artist_details(name):
    token = get_token()
    artist = search_for_artist(token, name)
    artist_id = get_artist_id(artist)
    print(get_artist_popularity(artist))

    print(f"{name}'s id: ", artist_id)

    songs = get_songs_by_artist(token, artist_id)
    #print(songs[0])
    print(datetime.date.today())
    print("Top 10")
    
    for i in range(len(songs)):
        print(i + 1, songs[i]["name"], songs[i]["popularity"])

    print("related genres:")
    print(get_related_genres(token, artist_id))

    print("related artists:")
    related_artist_details = get_related_artists(token, artist_id)['artists']
    related_artists = []
    for i in range(len(related_artist_details)):
        related_artists.append(related_artist_details[i]['name'])
    print(related_artists)

    print("top song:")
    top_song_id = songs[0]["id"]
    song_features = get_song_features(token, top_song_id)

    for key, value in song_features.items(): 
        print(f"{key}: {value}")

#get_artist_details("rio da yung og")
#get_artist_details("azel rm")
#get_artist_details("downtown kayoto")


def aggregate_artists(name):
    token = get_token()
    artist = search_for_artist(token, name)
    artist_id = get_artist_id(artist)

    print(f"{name}'s id: ", artist_id)

    print("related artists:")
    related_artist_details = get_related_artists(token, artist_id)['artists']
    related_artists = []
    for i in range(len(related_artist_details)):
        related_artists.append(related_artist_details[i]['name'])
    #print(related_artists)

    copy = related_artists.copy()
    final_set = set(related_artists.copy())

    for i in range(len(copy)):
        new_name = copy[i]
        a = search_for_artist(token, new_name)
        a_id = get_artist_id(a)

        related_a_details = get_related_artists(token, a_id)['artists']
        related_a = []

        for i in range(len(related_a_details)):
            final_set.add(related_a_details[i]['name'])
        

    print(final_set)

    lowest_p = 100
    lowest_p_artist = ""
    l = list(final_set)

    for i in range(len(final_set)):
        a = l[i]
        current = search_for_artist(token, a)
        current_popularity = get_artist_popularity(current)
        if current_popularity<lowest_p:
            lowest_p = current_popularity
            lowest_p_artist = current['name']

    print(lowest_p_artist)

aggregate_artists('mdma')








    


















