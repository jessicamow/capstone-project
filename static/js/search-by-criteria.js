document.querySelector('#search-by-criteria form').addEventListener('submit', (evt) => {
    evt.preventDefault();
  
    const streamingService = document.querySelector("#streaming").value;
    const genre = document.querySelector("#genre").value;
    const mediaType = document.querySelector(".media_type:checked").value;

    fetch(`/search-results?media_type=${mediaType}&streaming=${streamingService}&genre=${genre}`)
        .then(response => response.json())
        .then(apiResponse => {
            if (apiResponse.success) {
              const searchResults = apiResponse.search_results;
              const insertResultsTitle = document.createElement("h2");
              insertResultsTitle.innerText = "Search Results"
              const resultsDiv = document.querySelector("#results");
              removeAllChildNodes(resultsDiv);
              resultsDiv.appendChild(insertResultsTitle)
              const insertRow = document.createElement("div")
              insertRow.setAttribute("class", "row")
              for (let i=0; i<searchResults.length; i++) {
                const insertCol = document.createElement("div");
                insertCol.setAttribute("class", "col-4 search-result-option")
                const insertTitle = document.createElement("p");
                insertTitle.innerHTML = `${searchResults[i][0]}`;
                const insertDescription = document.createElement("p");
                insertDescription.innerHTML = `${searchResults[i][1]}`;
                const form = document.createElement("form");
                const submit = document.createElement("button");
                submit.setAttribute("type", "submit");
                submit.setAttribute("name", "title")
                results = searchResults[i][0].split(",")
                submit.setAttribute("value", `${[searchResults[i][0]]}`);
                submit.setAttribute("id", `search-results-${searchResults[i][0]}`);
                submit.innerText = "View Trailer";
                form.appendChild(submit);
                insertCol.appendChild(insertTitle)
                insertCol.appendChild(insertDescription)
                insertCol.appendChild(form)

                form.addEventListener('click', (evt) => {
                    evt.preventDefault();

                    fetch(`/select-${searchResults[i][2]}?title=${searchResults[i][0]}`)
                    .then(response => response.json())
                    .then(apiResponse => {
                        return_trailer(apiResponse);    
                    })
                })
                insertRow.appendChild(insertCol)
                }
                resultsDiv.appendChild(insertRow)
            } else {
              document.querySelector("#results").innerText = apiResponse.message;
            }
        })
});


document.querySelector('#select-tv form').addEventListener('submit', (evt) => {
    evt.preventDefault();
  
    const tv_title= document.querySelector("#tv-title").value;
    fetch(`/select-tv?title=${tv_title}`)
        .then(response => response.json())
        .then(apiResponse => {
            return_trailer(apiResponse);
        })
});

document.querySelector('#select-movie form').addEventListener('submit', (evt) => {
    evt.preventDefault();
  
    const movie_title= document.querySelector("#movie-title").value;
    fetch(`/select-movie?title=${movie_title}`)
        .then(response => response.json())
        .then(apiResponse => {
            return_trailer(apiResponse);
        })
});

function return_trailer(apiResponse) {
    if (apiResponse.success) {
        trailerURL = apiResponse.media_data[0];
        mediaName = apiResponse.media_data[1];
        mediaType = apiResponse.media_data[2];
        mediaID = apiResponse.media_data[3];
        watchStatus = apiResponse.media_data[4];
        mediaGenres = apiResponse.media_data[5];
        mediaStreaming = apiResponse.media_data[6];
        const resultsDiv = document.querySelector("#results");
        removeAllChildNodes(resultsDiv);

        const insertMediaTitle = document.createElement("h2");
        insertMediaTitle.setAttribute("class", "trailer-title")
        insertMediaTitle.innerHTML = `Trailer for ${mediaName}`;
        const insertTrailer = document.createElement("p");
        const trailerResponse = document.createElement("div")
        trailerResponse.setAttribute("class", "row")
        const trailerDiv = document.createElement("div")
        trailerDiv.setAttribute("class", "trailer")
        trailerDiv.setAttribute("class", "col-8")
        const trailer = document.createElement("iframe");
        trailer.setAttribute("width", "760");
        trailer.setAttribute("height", "400");
        trailer.setAttribute("src", `${trailerURL}`);
        trailer.setAttribute("frameborder", "0");
        trailer.setAttribute("allowfullscreen", "true");
        insertTrailer.appendChild(trailer);
        trailerDiv.appendChild(insertTrailer)
        const trailerOptionsDiv = document.createElement("div");
        trailerOptionsDiv.setAttribute("class", "col-4 trailer-options");
        const addBreak = document.createElement("br");
        const similarMediaDiv = document.createElement("div");
        const similarMediaForm = document.createElement("form");
        const similarMediaButton = document.createElement("button");
        similarMediaButton.setAttribute("type", "submit");
        similarMediaButton.innerText = "Click To View Another Recommendation";
        similarMediaForm.appendChild(similarMediaButton);
        similarMediaDiv.appendChild(similarMediaForm)
        const watchlistDiv = document.createElement("div")
        const watchlistForm = document.createElement("form");
        const watchlistInput = document.createElement("input");
        watchlistInput.setAttribute("type", "text");
        watchlistInput.setAttribute("name", "watchlist-name");
        watchlistInput.setAttribute("placeholder", "Watchlist Name")
        const watchlistButton = document.createElement("button");
        watchlistButton.setAttribute("type", "submit");
        watchlistButton.setAttribute("name", "media-data");
        watchlistButton.setAttribute("value", apiResponse.media_data);
        watchlistButton.innerText = "Add To Watchlist";
        watchlistForm.appendChild(watchlistInput);
        watchlistForm.appendChild(watchlistButton);
        watchlistDiv.appendChild(watchlistForm)
        trailerOptionsDiv.appendChild(similarMediaDiv)
        trailerOptionsDiv.appendChild(addBreak)
        trailerOptionsDiv.appendChild(watchlistDiv)
        trailerResponse.appendChild(trailerDiv)
        trailerResponse.appendChild(trailerOptionsDiv)
        resultsDiv.appendChild(insertMediaTitle);
        resultsDiv.appendChild(trailerResponse)
        similarMediaForm.addEventListener('submit', (evt) => {
            evt.preventDefault();

            fetch(`/similar-media/${mediaType}/${mediaID}`)
            .then(response => response.json())
            .then(apiResponse => {
                return_trailer(apiResponse);    
            })
        })
        watchlistForm.addEventListener('submit', (evt) => {
            evt.preventDefault();

            fetch(`/add-to-watchlist?watchlist-name=${watchlistInput.value}&media-data=${watchlistButton.value}`)
            .then(response => response.json())
            .then(response => {
                removeAllChildNodes(watchlistDiv)
                const watchlistMsg = document.createElement("p")
                watchlistMsg.setAttribute("class", "trailer-options")
                watchlistMsg.innerHTML = `${response.message}`
                watchlistDiv.appendChild(watchlistMsg)
            })
        })
      } else {
        document.querySelector("#results").innerText = apiResponse.message;
      }
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}