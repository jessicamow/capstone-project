document.querySelector('#search-by-criteria form').addEventListener('submit', (evt) => {
    evt.preventDefault();
  
    
    const streamingService = document.querySelector("#streaming").value;
    const genre = document.querySelector("#genre").value;
    const mediaType = document.querySelector(".media_type:checked").value;
    console.log(media_type)
    fetch(`/search-results?media_type=${mediaType}&streaming=${streamingService}&genre=${genre}`)
    document.querySelector('#results').innerHTML = media_type;
});