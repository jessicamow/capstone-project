document.querySelector("#filter-by-criteria form").addEventListener('submit', (evt) => {
    evt.preventDefault();

    const filterGenre = document.querySelector("#filter-genre").value;
    const filterStreaming = document.querySelector("#filter-streaming").value;
    const filterType = document.querySelector(".filter-media-type:checked").value;
    fetch(`/filter-media?filter_type=${filterType}&filter_genre=${filterGenre}&filter_streaming=${filterStreaming}`)
        .then(response => response.json())
        .then(response => {
            if (response.success) {
                // console.log(response.friends_media)
                const resultsDiv = document.querySelector("#media-results");
                removeAllChildNodes(resultsDiv)
                const insertRow = document.createElement("div")
                insertRow.setAttribute("class", "row")
                for([media_name, info] of Object.entries(response.friends_media))  {
                    const insertCol = document.createElement("div")
                    insertCol.setAttribute("class", "col-4 media-from-friends")
                    const mediaRow = document.createElement("div")
                    mediaRow.setAttribute("class", "row")
                    // const titleCol = document.createElement("div")
                    // titleCol.setAttribute("class", "col")
                    const insertTitle = document.createElement("p");
                    insertTitle.innerHTML = `${media_name}`;
                    // titleCol.appendChild(insertTitle)
                    mediaRow.appendChild(insertTitle)
                    // resultsDiv.appendChild(insertTitle)
                    const users = []
                    const watch_statuses = []
                    // console.log(info.type)
                    for ([key, val] of Object.entries(info.user_info)) {
                        // console.log("key", key)
                        // console.log("value", val)
                        users.push(val.user_name)
                        watch_statuses.push(val.watch_status)
                    }
                    // console.log(users)
                    // console.log(watch_statuses)
                    const userCol = document.createElement("div")
                    userCol.setAttribute("class", "col-6")
                    const insertUser = document.createElement("p");
                    insertUser.innerHTML = "User Watching:";
                    userCol.appendChild(insertUser)
                    mediaRow.appendChild(userCol)
                    const statusCol = document.createElement("div")
                    statusCol.setAttribute("class", "col-6")
                    const insertStatus = document.createElement("p");
                    insertStatus.innerHTML = "Watch Status:";
                    statusCol.appendChild(insertStatus)
                    mediaRow.appendChild(statusCol)
                    const userInfoCol = document.createElement("div")
                    userInfoCol.setAttribute("class", "col-6")
                    for (let i=0; i < users.length; i++) {
                        let addUser = document.createElement("p");
                        if (users[i] == response.logged_user) {
                            addUser.setAttribute("class", "your-media")
                            addUser.innerHTML = "You are watching this show!"
                        }
                        else {
                            addUser.innerHTML = `${users[i]}`
                        }
                        userInfoCol.appendChild(addUser)
                    }
                    mediaRow.appendChild(userInfoCol)
                    const statusInfoCol = document.createElement("div")
                    statusInfoCol.setAttribute("class", "col-6")
                    for (let i=0; i < watch_statuses.length; i++) {
                        let addStatus = document.createElement("p");
                        addStatus.innerHTML = `${watch_statuses[i]}`
                        statusInfoCol.appendChild(addStatus)
                    }
                    mediaRow.appendChild(statusInfoCol)
                    if (users.includes(response.logged_user)) {
                        const discussion = document.createElement("form");
                        discussion.setAttribute("action", "/view-discussion-threads")
                        const discussionSubmit = document.createElement("button");
                        discussionSubmit.setAttribute("type", "submit");
                        discussionSubmit.setAttribute("name", "media-name")
                        discussionSubmit.setAttribute("value", `${media_name}`);
                        // submit.setAttribute("id", `search-results-${result[0]}`);
                        discussionSubmit.innerText = "See Discussion Threads";
                        discussion.appendChild(discussionSubmit);
                        mediaRow.appendChild(discussion)
                        insertCol.append(mediaRow)
                    }
                    else {
                        const addBreak = document.createElement("br");
                        console.log("part1:", info.type, media_name)
                        const watchlistDiv = document.createElement("div");
                        const watchlist = document.createElement("form");
                        const inputText = document.createElement("input");
                        inputText.setAttribute("type", "text");
                        inputText.setAttribute("name", "watchlist-name");
                        inputText.setAttribute("placeholder", "Watchlist Name")
                        const submit = document.createElement("button");
                        submit.setAttribute("type", "submit");
                        submit.setAttribute("name", "media-info")
                        submit.setAttribute("value", `${media_name}~${info.type}`);
                        // submit.setAttribute("id", `search-results-${result[0]}`);
                        submit.innerText = "Add To Watchlist";
                        watchlist.appendChild(inputText)
                        watchlist.appendChild(submit);
                        watchlistDiv.appendChild(watchlist)
                        watchlistDiv.appendChild(addBreak)
                        mediaRow.appendChild(watchlistDiv)

                        const discussion = document.createElement("form");
                        discussion.setAttribute("action", "/view-discussion-threads")
                        const discussionSubmit = document.createElement("button");
                        discussionSubmit.setAttribute("type", "submit");
                        discussionSubmit.setAttribute("name", "media-name")
                        discussionSubmit.setAttribute("value", `${media_name}`);
                        // submit.setAttribute("id", `search-results-${result[0]}`);
                        discussionSubmit.innerText = "See Discussion Threads";
                        discussion.appendChild(discussionSubmit);
                        
                        mediaRow.appendChild(discussion)
                        // resultsDiv.appendChild(discussion)

                        watchlist.addEventListener("submit", (evt) => {
                            evt.preventDefault();
    
                            console.log(submit.value)
                            const selected_media = submit.value.split("~")
                            console.log(`/select-${selected_media[1]}?title=${selected_media[0]}`)
    
                            fetch(`/select-${selected_media[1]}?title=${selected_media[0]}`)
                            .then(response => response.json())
                            .then(response => {
                                console.log(response)
                                if (response.success) {
                                    const media_data = response.media_data;
    
                                    fetch(`/add-to-watchlist?watchlist-name=${inputText.value}&media-data=${media_data}`)
                                    .then(response => response.json())
                                    .then(watchlistResponse => {
                                        removeAllChildNodes(watchlistDiv)
                                        const watchlistMsg = document.createElement("p");
                                        watchlistMsg.innerText = `${watchlistResponse.message}`
                                        watchlistDiv.appendChild(watchlistMsg)
                                        console.log(watchlistResponse)
                                        console.log(watchlistResponse.message)
                                    })
                                }
                            })
    
                            
                        })
                        insertCol.append(mediaRow)
                    }
                    insertRow.appendChild(insertCol)
                }
                resultsDiv.appendChild(insertRow)
            }
        })
});

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}