# Buscar un artista y devolver todos sus ábulmes y hits más populares

import requests

def get_artist_id(artist_name, access_token):
    url = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if data['artists']['items']:
        return data['artists']['items'][0]['id']
    return None

def get_artist_albums(artist_name, access_token):
    artist_id = get_artist_id(artist_name, access_token)
    if artist_id:
        url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        return response.json()['items']
    return None

if __name__ == "__main__":
    access_token = 'BQDHpU06ywcdHD1gaak9YORUCCGBYROgdTYHYQfI7tX3TG6jnp6Jg_uM5U92YohdTPDWTKsFZMc4AefUKTmRtd8ClvPiX3qlFWShND7skapdoC4ShZk'
    artist_name = input("Introduce el nombre del artista: ")
    albums = get_artist_albums(artist_name, access_token)
    if albums:
        for album in albums:
            print(album['name'])
    else:
        print("No se encontraron álbums para el artista.")
