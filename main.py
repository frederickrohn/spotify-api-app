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

    print((songs))

    for i in range(len(songs)):
        print(i, songs[i]["name"], songs[i]["popularity"])

test_get_songs()
















