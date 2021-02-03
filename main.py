from flask import Flask, render_template
import requests
import os
import random
from dotenv import load_dotenv, find_dotenv




load_dotenv(find_dotenv())

auth_url = "https://accounts.spotify.com/api/token"

auth_response = requests.post(auth_url,{
    'grant_type': 'client_credentials',
    'client_id': os.getenv('SPOTIFTY_ID'),
    'client_secret': os.getenv('SPOTIFY_SECRET')
})
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']


#url = "https://api.spotify.com/v1/browse/new-releases?country=US&limit=10"
artists = ["1hNaHKp2Za5YdOAG0WnRbc", "4Ns55iOSe1Im2WU2e1Eym0", "6vWDO969PvNqNYHIOW5v0m"]
names = {"1hNaHKp2Za5YdOAG0WnRbc": "Tiwa Savage", "4Ns55iOSe1Im2WU2e1Eym0": "Simi", "6vWDO969PvNqNYHIOW5v0m": "Beyonce"}
artist_id = artists[random.randint(0,2)]
url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
response = requests.get(
    url,
    headers=headers
)

data = response.json()
song = random.choice(data['tracks'])
print(song['name'] + " by " + names[artist_id]) 