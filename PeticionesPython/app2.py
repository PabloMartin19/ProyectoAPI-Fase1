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

def get_artist_id(artist_name, access_token):
    url = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code != 200:
        print(f"Error en la búsqueda del artista: {data}")
        return None
    if data['artists']['items']:
        return data['artists']['items'][0]['id']
    return None

def get_artist_albums(artist_name):
    access_token = get_access_token()
    if not access_token:
        return None
    artist_id = get_artist_id(artist_name, access_token)
    if artist_id:
        url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error en la obtención de álbumes: {response.json()}")
            return None
        return response.json()['items']
    return None

if __name__ == "__main__":
    artist_name = input("Introduce el nombre del artista: ")
    albums = get_artist_albums(artist_name)
    if albums:
        for album in albums:
            print(album['name'])
    else:
        print("No se encontraron álbums para el artista.")
