from flask import Flask, render_template
import requests
import os
import random
from dotenv import load_dotenv, find_dotenv
from urllib.parse import quote

load_dotenv(find_dotenv())


#Getting Spotify authorization token:
def get_auth_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(auth_url,{
    'grant_type': 'client_credentials',
    'client_id': os.getenv('SPOTIFY_ID'),
    'client_secret': os.getenv('SPOTIFY_SECRET')
    })
    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

#Getting a song with Spotify API:
def get_random_track(artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = {'Authorization': 'Bearer {token}'.format(token=get_auth_token())}
    response = requests.get(
        url,
        headers=headers
    )
    if response.ok and len(response.text) > 0:
        data = response.json()
        return random.choice(data['tracks']) #Choose a random song from the list of artist's most popular songs
    return ''

#Getting additional song info:
def get_beat_length(song_id):
    url2 = f'https://api.spotify.com/v1/audio-features?ids={song_id}'
    response = requests.get(
        url2,
        headers={'Authorization': 'Bearer {token}'.format(token=get_auth_token())}
    )
    if response.ok and len(response.text) > 0:
        song_info_data = response.json()
        tempo = song_info_data['audio_features'][0]['tempo']
        if len(song_info_data['audio_features']) > 0:
            return str(60/tempo) #to calculate the length of 1 beat in the song in seconds
    return '1.5'

#Getting artist picture:    
def get_artist_img(artist_id):
    url3 = f"https://api.spotify.com/v1/artists/{artist_id}"
    response = requests.get(
        url3,
        headers={'Authorization': 'Bearer {token}'.format(token=get_auth_token())}
    )

    if response.ok and len(response.text) > 0:
        artist_info = response.json()
        if len(artist_info['images']) > 0:
            return artist_info['images'][0]['url']
    return 'https://www.civhc.org/wp-content/uploads/2018/10/question-mark-768x768.png'

#Search for an artist id by artist name:
def get_artist_id(artist_name):
    serialized_name = quote(artist_name)
    url = f"https://api.spotify.com/v1/search?q={serialized_name}&type=artist&market=US&limit=1"
    response = requests.get(
        url,
        headers={'Authorization': 'Bearer {token}'.format(token=get_auth_token())}
        )
    if response.ok and len(response.text) > 0:
        search_results = response.json()
        if len(search_results['artists']['items']) > 0:
            return [ search_results['artists']['items'][0]['id'], search_results['artists']['items'][0]['name'] ]
    return '6XpaIBNiVzIetEPCWDvAFP' #return Whitney Houston by default
        
 
#Using Genius API for lyrics:
def get_lyrics(song_title, artist_name):
    song_search = quote(f"{song_title} {artist_name}") #quote() serializes the string so it cn be used in the search query
    genius_url = f"https://api.genius.com/search?q={song_search}"
    lyrics_response = requests.get(
        genius_url,
        headers={'Authorization': 'Bearer {token}'.format(token=os.getenv('GENIUS_ACCESS_TOKEN'))}
    )

    if lyrics_response.ok and len(lyrics_response.text) > 0:
        lyrics_data = lyrics_response.json()
        if len(lyrics_data['response']['hits']) > 0:
            return lyrics_data['response']['hits'][0]['result']['url']
    return ''

    
access_token = get_auth_token()
    
#default values:
p_url_exists = False
preview_url = ''
l_url_exists = False
lyrics_url = ''

artists = ['1hNaHKp2Za5YdOAG0WnRbc', '4Ns55iOSe1Im2WU2e1Eym0', '6vWDO969PvNqNYHIOW5v0m', '5MEHQvTW53C0ccsuxdZobQ', '3ukrG1BmfEiuo0KDj8YTTS', '7fKO99ryLDo8VocdtVvwZW']
names = {'1hNaHKp2Za5YdOAG0WnRbc': 'Tiwa Savage', '4Ns55iOSe1Im2WU2e1Eym0': 'Simi', '6vWDO969PvNqNYHIOW5v0m': 'Beyonce', '5MEHQvTW53C0ccsuxdZobQ': 'Niniola', '3ukrG1BmfEiuo0KDj8YTTS': 'Teni', '7fKO99ryLDo8VocdtVvwZW': 'Yemi Alade'}


artist_id = artists[random.randint(0,5)] #choose 1 of the 6 artists randomly
artist_name = names[artist_id]

song = get_random_track(artist_id)
if song == '':
    song_title = 'Oh no! :('
    song_img_src = 'https://www.clipartkey.com/mpngs/m/36-364563_crying-sad-emoji-png-sad-face-emoji-transparent.png'
    preview_url = ''
    artist_name = "Not an Actual Artist..."
    lyrics_url = ''

song_title = song['name']
song_img_src = song['album']['images'][0]['url']
artist_img_src = get_artist_img(artist_id)

if isinstance(song['preview_url'], str):
    preview_url = song['preview_url']
    p_url_exists = True
       
if p_url_exists and song != '':
    song_id = song['id']
    beat_length = get_beat_length(song_id)
    lyrics_url = get_lyrics(song_title, artist_name)
    if len(lyrics_url) > 0:
        l_url_exists = True
else:
    beat_length = '1.5'


#Using Flask to pass variables to html:
app = Flask(__name__)
@app.route('/')
def song_info():
     return render_template('index.html', song_title = song_title, artist_name = artist_name, preview_url = preview_url, p_url_exists = p_url_exists, song_img_src = song_img_src, artist_img_src = artist_img_src, beat_length = beat_length, lyrics_url = lyrics_url, l_url_exists = l_url_exists)

@app.route('/search/<name>')
def search(name):
    artist_id = get_artist_id(name)[0]
    artist_name = get_artist_id(name)[1]
    
    if(get_random_track(artist_id) == ''):
        song_title = 'Oh no! :('
        artist_name = "Not an Actual Artist..."
        preview_url = ''
        p_url_exists = False
        song_img_src = 'https://www.clipartkey.com/mpngs/m/36-364563_crying-sad-emoji-png-sad-face-emoji-transparent.png'
        artist_img_src = 'https://www.civhc.org/wp-content/uploads/2018/10/question-mark-768x768.png'
        beat_length = '1.5'
        lyrics_url = ''
        l_url_exists = False
    else:
        song = get_random_track(artist_id)
        song_title = song['name']
        song_img_src = song['album']['images'][0]['url']
        artist_img_src = get_artist_img(artist_id)
        if isinstance(song['preview_url'], str):
            preview_url = song['preview_url']
            p_url_exists = True
            song_id = song['id']
            beat_length = get_beat_length(song_id)
            lyrics_url = get_lyrics(song_title, artist_name)
            if len(lyrics_url) > 0:
                l_url_exists = True
            else:
                l_url_exists = False
        else:
            preview_url = ''
            p_url_exists = False
            beat_length = '1.5'
            lyrics_url = ''
            l_url_exists = False
    return{
            'song_title': song_title,
            'artist_name': artist_name,
            'preview_url': preview_url,
            'p_url_exists': p_url_exists,
            'song_img_src': song_img_src,
            'artist_img_src': artist_img_src,
            'beat_length': beat_length,
            'lyrics_url': lyrics_url,
            'l_url_exists': l_url_exists,
    }
        

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #So style.css refreshes
app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0'),
    debug=True
    )
