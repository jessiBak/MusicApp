# Project 1

## Requirements
* `pip install flask`
* `pip install requests`
* `pip install python-dotenv`
* Spotify Client ID and Secret keys (Follow instructions at https://developer.spotify.com/documentation/web-api/quick-start/ to get them)

## Setup
1. Create .env file in main directory
2. Add Spotify keys with the lines:
```export SPOTIFTY_ID="YOUR_CLIENT_ID_HERE" 
export SPOTIFY_SECRET="YOUR_SECRET_KEY_HERE"
```
   
## Running the Application
1. Run this command in the terminal: `python main.py`
2. See one of an artist's most popular songs and listen to a preview, if available.
3. An image of the artist will pulse to the beat of the preview song!

## Technical Issues Encountered
1. Originally, all the song-related images would appear to be broken, even when clicking the src url would display the image properly in a new tab.
*  I was able to fix this by comparing the official Flask documentation's syntax of getting variable values in an html file with my own.
* I realized that instead of `<img src={{song_img_src}}/>`, I should have used `<img src={{song_img_src}} />`.
2. Initially, the Song title and artist name texts and the song-related image weren't aligned with each other
* I looked up how to align elements with CSS using this website (https://www.geeksforgeeks.org/css-centering-elements/)
* Using that information, I was able to vertically align the headers, image, and song preview audio elements
3. There would occasionally the app would be unable to be accessed through a browser.
* After looking at the Spotify documentation, I noticed that not every song would have a preview url. Whenever the preview url was null, a runtime error would occur.
* This meant that I had to add a conditional statement to account for null preview urls by displaying a message indicating the preview was unavailable.

## Additional Features
* I'm considering displaying 3 random songs from an artist in a carousel style using CSS animations
* I'd also like to have the user see a link to the artist's Spotify page if they hover over the artist's picture. I'd likely need some JavaScript functions for that.
* I'd also like to improve the artist image pulse animation with more CSS animations