from flask import Flask, render_template
import requests
import os
import random
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

#Getting authorization token
auth_url = "https://accounts.spotify.com/api/token"
auth_response = requests.post(auth_url,{
    'grant_type': 'client_credentials',
    'client_id': os.getenv('SPOTIFTY_ID'),
    'client_secret': os.getenv('SPOTIFY_SECRET')
})
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']


#Getting a song
artists = ['1hNaHKp2Za5YdOAG0WnRbc', '4Ns55iOSe1Im2WU2e1Eym0', '6vWDO969PvNqNYHIOW5v0m']
names = {'1hNaHKp2Za5YdOAG0WnRbc': 'Tiwa Savage', '4Ns55iOSe1Im2WU2e1Eym0': 'Simi', '6vWDO969PvNqNYHIOW5v0m': 'Beyonce'}

artist_id = artists[random.randint(0,2)] #choose 1 of the 3 artists randomly

url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
response = requests.get(
    url,
    headers=headers
)

data = response.json()
song = random.choice(data['tracks']) #Choose a random song from the list of artist's most popular songs

p_url_exists = False
song_title = song['name']
artist_name = names[artist_id]
preview_url = ''
if isinstance(song['preview_url'], str):
    preview_url = song['preview_url']
    p_url_exists = True
    
song_img_src = song['album']['images'][0]['url']

#Getting additional song info:
if(p_url_exists):
    song_id = song['id']
    url2 = f'https://api.spotify.com/v1/audio-features?ids={song_id}'
    response = requests.get(
        url2,
        headers=headers
    )
    if(response.json()):
        song_info_data = response.json()
        tempo = song_info_data['audio_features'][0]['tempo']
        beat_length = str(60/tempo) #to calculate the length of 1 beat in the song in seconds
else:
    beat_length = 0

#Getting artist picture:
url3 = f"https://api.spotify.com/v1/artists/{artist_id}"
response = requests.get(
    url3,
    headers=headers
)

artist_info = response.json()
artist_img_src = artist_info['images'][0]['url']


#Using Flask to pass variables to html
app = Flask(__name__)
@app.route('/')
def song_info():
     return render_template('index.html', song_title = song_title, artist_name = artist_name, preview_url = preview_url, song_img_src = song_img_src, artist_img_src = artist_img_src, beat_length = beat_length)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #So style.css refreshes
app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0'),
    debug=True
    )
