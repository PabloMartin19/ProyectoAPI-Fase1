# Buscar una canción y devolver el álbum al que pertenece y el artista que la hizo

import requests
from KEY import get_access_token

def search_song(song_name, access_token):
    url = f'https://api.spotify.com/v1/search?q={song_name}&type=track'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if data['tracks']['items']:
        return data['tracks']['items'][0]
    return None

def get_song_info(song_name):
    access_token = get_access_token()
    if not access_token:
        return None
    song_info = search_song(song_name, access_token)
    if song_info:
        album_name = song_info['album']['name']
        artist_name = song_info['artists'][0]['name']
        return {
            'song_name': song_info['name'],
            'album_name': album_name,
            'artist_name': artist_name
        }
    return None

if __name__ == "__main__":
    song_name = input("Introduce el nombre de la canción: ")
    song_info = get_song_info(song_name)
    if song_info:
        print(f"Song: {song_info['song_name']}")
        print(f"Album: {song_info['album_name']}")
        print(f"Artist: {song_info['artist_name']}")
    else:
        print("Canción no encontrada.")



