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

def get_album_id(album_name, access_token):
    url = f'https://api.spotify.com/v1/search?q={album_name}&type=album'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code != 200:
        print(f"Error en la búsqueda del álbum: {data}")
        return None
    if data['albums']['items']:
        return data['albums']['items'][0]['id']
    return None

def get_album_tracks(album_name):
    access_token = get_access_token()
    if not access_token:
        return None
    album_id = get_album_id(album_name, access_token)
    if album_id:
        url = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error en la obtención de canciones: {response.json()}")
            return None
        return response.json()['items']
    return None

if __name__ == "__main__":
    album_name = input("Introduce el nombre del álbum: ")
    tracks = get_album_tracks(album_name)
    if tracks:
        for track in tracks:
            print(track['name'])
    else:
        print("No se encontraron canciones para el álbum.")
