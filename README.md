# Project 1: A Music Discovery App!

See it deployed here: https://secret-chamber-08624.herokuapp.com/ 

## Requirements
* `pip install flask`
* `pip install requests`
* `pip install python-dotenv`
* Spotify Client ID and Secret keys (Follow instructions at https://developer.spotify.com/documentation/web-api/quick-start/ to get them)
* Genius Access Token (Follow instructions at https://docs.genius.com/#/getting-started-h1 to get it)

## Setup
1. Create .env file in main directory
2. Add Spotify keys and Genius access token with the lines:
```
export SPOTIFY_ID="YOUR_CLIENT_ID_HERE" 
export SPOTIFY_SECRET="YOUR_SECRET_KEY_HERE"
export GENIUS_ACCESS_TOKEN="YOUR_ACCESS_TOKEN_HERE"
```
   
## Running the Application
1. Run this command in the terminal: `python main.py`
2. See one of an artist's most popular songs and listen to a preview, if available.
3. An image of the artist will pulse to the beat of the preview song!
4. You can also search for an artist by name and see a random song from that artist's top tracks.

## Technical Issues Encountered
1. Originally, all the song-related images would appear to be broken, even when clicking the src url would display the image properly in a new tab.
*  I was able to fix this by comparing the official Flask documentation's syntax of getting variable values in an html file with my own.
* I realized that instead of `<img src={{song_img_src}}/>`, I should have used `<img src={{song_img_src}} />`.
2. Initially, the Song title and artist name texts and the song-related image weren't aligned with each other
* I looked up how to align elements with CSS using this website (https://www.geeksforgeeks.org/css-centering-elements/)
* Using that information, I was able to vertically align the headers, image, and song preview audio elements
3. Occasionally the app would be unable to be accessed through a browser.
* After looking at the Spotify documentation, I noticed that not every song would have a preview url. Whenever the preview url was null, a runtime error would occur.
* This meant that I had to add a conditional statement to account for null preview urls by displaying a message indicating the preview was unavailable.
4. I wanted to apply a filter to a background image I used for the music_info div, but when using a filter applied to all the elements within the div.
* This answer from StackOverflow was extremely helpful: https://stackoverflow.com/questions/58207753/how-do-i-apply-a-css-filter-to-only-the-background-image
* This website helped me calculate the filter I needed based on the color: https://codepen.io/sosuke/pen/Pjoqqp
* After wrapping the music_info into another div meant to hold the background image, I was able to apply the filter using the code in the StackOverflow answer as a basis.

## Additional Features and Known Issues
* I'd like to display 3 random songs from an artist in a carousel style using CSS animations and/or JavaScript
* This resource seems like it would be helpful in learning how to do this with just CSS: https://speckyboy.com/open-source-carousel-sliders-css/
* I'd also like to have the user see a link to the artist's Spotify page if they hover over the artist's picture. I'd likely need some JavaScript functions and on hover attributes for that.
* I'd also like to improve the artist image pulse animation with more CSS animations

* One known issue is that if a user searches for a new song with available lyrics, the link to the lyrics would open in a new window before the rest of the page loads.
* Additionally, clicking the lyrics button would not do anything after this occurs.
* This most likely has something to do with how I replaced the lyrics link url with JavaScript.
