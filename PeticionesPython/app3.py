# Buscar un álbum y devolver las canciones que contiene

import requests

def get_album_id(album_name, access_token):
    url = f'https://api.spotify.com/v1/search?q={album_name}&type=album'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if data['albums']['items']:
        return data['albums']['items'][0]['id']
    return None

def get_album_tracks(album_name, access_token):
    album_id = get_album_id(album_name, access_token)
    if album_id:
        url = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        return response.json()['items']
    return None

if __name__ == "__main__":
    access_token = 'BQDHpU06ywcdHD1gaak9YORUCCGBYROgdTYHYQfI7tX3TG6jnp6Jg_uM5U92YohdTPDWTKsFZMc4AefUKTmRtd8ClvPiX3qlFWShND7skapdoC4ShZk'
    album_name = input("Introduce el nombre del álbum: ")
    tracks = get_album_tracks(album_name, access_token)
    if tracks:
        for track in tracks:
            print(track['name'])
    else:
        print("No se encontraron canciones para el álbum.")
