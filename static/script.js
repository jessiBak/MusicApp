window.onload = () => { // onload makes sure the content is loaded on page first
    document.getElementById('submit').addEventListener('click', () => {
        // Everything you want to do when button is clicked below
        console.log('Button was clicked!');
        const userText = document.getElementById('search').value;
        const url = '/search/' + userText; 
        window.fetch(url) 
        .then(response => response.json())
        .then(data => { // .then will only run the function *once* the data is fetched from the internet
        console.log(data);
        
        //replace with new song title
        const newH2 = document.createElement('h2');
        let h2txt = document.createTextNode(data['song_title']);
        newH2.appendChild(h2txt);
        const h2_item = document.querySelector('h2');
        h2_item.parentNode.replaceChild(newH2, h2_item);
        
        //replace with new artist name
        const newH3 = document.createElement('h3');
        let h3txt = document.createTextNode('By ' + data['artist_name']);
        newH3.appendChild(h3txt);
        const h3_item = document.querySelector('h3');
        h3_item.parentNode.replaceChild(newH3, h3_item);
        
        //replace with new artist image src
        const old_a_img = document.querySelector('.round');
        old_a_img.src = data['artist_img_src']; 
        let ani = "pulse " + data['beat_length'] + "s infinite";
        old_a_img.style.animation =  ani;
        
        //replace with new preview url
        const old_audio = document.querySelector('audio');
        if (typeof(old_audio) != 'undefined' && old_audio != null) //there was originally a preview 
        {
            if(data['p_url_exists'])//if new song also has preview, replace src url
            {
                old_audio.src = data['preview_url'];
            }
            else//if new song doesnt have preview, replace old audio with h3 preview unavailable message
            {
                const newErrorh3 = document.createElement('h3');
                let errortxt = document.createTextNode('Preview unavailable :\(');
                newErrorh3.appendChild(errortxt);
                newErrorh3.style.color = '#8014f';
                newErrorh3.style.fontFamily = 'Courgette';
                old_audio.parentNode.replaceChild(newErrorh3, old_audio);
                
            }
        }
        else//old audio doesnt exist, so create audio if preview url or h3 wih error message and replace old h3 with one of those
        {
            if(data['p_url_exists'])
            {
                const new_audio = document.createElement('audio');
                new_audio.controls = 'controls';
                new_audio.src = data['preview_url'];
                new_audio.style.marginLeft = 'auto';
                new_audio.style.marginRight = 'auto';
                new_audio.style.display = 'block';
                new_audio.style.filter = 'invert(72%) sepia(10%) saturate(2506%) hue-rotate(178deg) brightness(100%) contrast(103%)';
                const old_h3_error = document.querySelector('#no_preview');
                old_h3_error.parentNode.replaceChild(new_audio, old_h3_error);
            }
        }
        
        //replace old song img with new one
        const old_song_img = document.querySelector('#song_img');
        old_song_img.src = data['song_img_src'];
        
        //replace old lyrics button (if it existed with new one if it exists)
        
        const old_lyrics = document.querySelector('#lyrics_button');
        if (typeof(old_lyrics) != 'undefined' && old_lyrics != null) //there was originally a link to the lyrics
        {
            if(data['l_url_exists'])
            {
                let click = window.open(data['lyrics_url'], '_blank');
                old_lyrics.onclick = String(click);
            }
        }
        else // have to add a new lyrics button, if there's a link to new lyrics
        {
            if(data['l_url_exists'])
            {
                const new_lyrics = document.createElement('button');
                new_lyrics.type = "button";
                new_lyrics.id = "lyrics_button"
                new_lyrics.onclick = "window.open('" + data['lyrics_url'] + "','_blank')";
                new_lyrics.textContent = "Click here for the lyrics!";
                const artist_div = document.querySelector('.artist');
                artist_div.appendChild(new_lyrics);
            }
        }

        
        });
     });
}; 