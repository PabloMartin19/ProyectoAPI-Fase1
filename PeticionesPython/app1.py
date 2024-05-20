import requests
import os
from requests.auth import HTTPBasicAuth

def get_access_token():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    if not client_id or not client_secret:
        print("Las credenciales no están disponibles")
        return None
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    if response.status_code != 200:
        print(f"Error en la petición: {response.status_code}")
        print(response.json())
        return None
    response_data = response.json()
    access_token = response_data.get('access_token')
    return access_token

def search_song(song_name, access_token):
    url = f'https://api.spotify.com/v1/search?q={song_name}&type=track'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code != 200:
        print(f"Error en la búsqueda de la canción: {data}")
        return None
    if data['tracks']['items']:
        return data['tracks']['items'][0]
    return None

def get_song_info(song_name):
    access_token = get_access_token()
    if not access_token:
        print("No se pudo obtener el token de acceso")
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
