import spotify_methods as sm

def convert_dict_item(token, artist_id):
    item = sm.search_for_artist_by_id(token, artist_id)
    return {artist_id: (item["popularity"], item["name"])}


def related_artists_as_dict(token, artist_id):
    list = sm.get_related_artists(token, artist_id)

    dict = {}

    for item in list:
        current = (item["popularity"], item["name"])
        dict[item["id"]] = current
    
    return dict

def test_related_artists_as_dict(name):
    t = sm.get_token()

    a = sm.search_for_artist_by_name(t, name)

    print(a["name"])

    dict = related_artists_as_dict(t, a["id"])

    for value in dict.values():
        print(value[1])
    

#test_related_artists_as_dict("icewear vezzo")

def find_related_arists_with_layers(token, artist_id, layers):
    dict = convert_dict_item(token, artist_id)
    for i in range(layers):
        copy = dict.copy()
        for key in copy:
            dict.update(related_artists_as_dict(token, key))

    return dict

def test_layered_find_related(name):
    t = sm.get_token()
    id = sm.search_for_artist_by_name(t, name)["id"]
    d = find_related_arists_with_layers(t, id, 2)

    for value in d.values():
        print(value[1], value[0])


#test_layered_find_related("BROCKHAMPTON")


def filter_artist_dictionary(dictionary):
    max = int(input("Enter maximum popularity: "))
    min = int(input("Enter minimum popularity: "))

    filtered_dict = {}
    for key, value in dictionary.items():
        if value[0] <= max and value[0] >= min:
            filtered_dict[key] = value
    return filtered_dict

def test_filter_artist_dictionary():
    t = sm.get_token()
    all_artists = find_related_arists_with_layers(t, sm.search_for_artist_by_name(t, "drake")['id'], 2)
    print("original size: ", len(all_artists))
    sorted = filter_artist_dictionary(all_artists)
    print("sorted size: ", len(sorted))
    for value in sorted.values():
        print(value[1], value[0])

# test_filter_artist_dictionary()













