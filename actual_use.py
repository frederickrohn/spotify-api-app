import spotify_methods as sm

from artist import Artist

t = sm.get_token()

def convert_to_object(token, artist_id):
    a = sm.search_for_artist_by_id()
    return Artist(a["name"], a["id"], a["popularity"])

def aggregate_related_artists(token, artist_name, levels):
    artist_list = sm.get_related_artists(token, original_artist)
    list_to_iterate = artist_list.copy()

    original_artist = sm.search_for_artist_by_name(token, artist_name)
    a_name = print(original_artist["name"])
    print(f"artists related to {a_name}: ")

    sm.get_related_artists(token, original_artist)






