document.querySelector("#new-discussion").addEventListener("click", (evt) => {
    evt.preventDefault();

    const discussion = document.querySelector("#add-discussion")
    removeAllChildNodes(discussion)

    const discussionPrompt = document.createElement("p")
    discussionPrompt.innerHTML = "Create a new discussion post!"
    const newDiscussion = document.createElement("form")
    const title = document.createElement("input")
    title.setAttribute("type", "textarea")
    title.setAttribute("name", "title")
    title.setAttribute("placeholder", "Thread Title")
    const post = document.createElement("input")
    post.setAttribute("type", "textarea")
    post.setAttribute("name", "post")
    post.setAttribute("placeholder", "Start your thread!")
    const submit = document.createElement("button");
    submit.setAttribute("type", "submit");
    submit.innerText = "Submit"
    newDiscussion.appendChild(title)
    newDiscussion.appendChild(post)
    newDiscussion.appendChild(submit)
    discussion.appendChild(discussionPrompt)
    discussion.appendChild(newDiscussion)

    submit.addEventListener("click", (evt) => {
        evt.preventDefault()
        fetch(`/add-discussion-threads?post=${post.value}&title=${title.value}`)
            .then(response => response.json())
            .then(response => {
                const insertUser = document.createElement("p")
                const insertNewThread = document.createElement("button")
                insertNewThread.setAttribute("type", "submit")
                insertNewThread.setAttribute("class", "discussion-button")
                insertNewThread.setAttribute("name", "discussion-button")
                insertNewThread.setAttribute("value", response.comment_id)
                insertNewThread.innerText = `${response.title}`
                insertUser.innerText = `${response.user} created thread: `
                insertUser.appendChild(insertNewThread)
                const discussionDiv = document.querySelector("#discussion")
                discussionDiv.appendChild(insertUser)
                title.value = ""
                post.value = ""
            })
    })
})

const allDiscussionThreads = document.querySelectorAll(".discussion-button")

for (const discussionThread of allDiscussionThreads) {
    discussionThread.addEventListener("click", (evt) => {
    evt.preventDefault()
    fetch(`/view-individual-thread?comment_id=${discussionThread.value}`)
        .then(response => response.json())
        .then(response => {
            if (response.success) {
                const discussionThread = document.querySelector("#discussion-thread")
                removeAllChildNodes(discussionThread)
                const insertTitle = document.createElement("h2")
                insertTitle.innerText = `Thread Title: ${response.title}`
                discussionThread.appendChild(insertTitle)
                const insertComment = document.createElement("p")
                insertComment.innerText = `${response.user_comment}: ${response.comment}`
                discussionThread.appendChild(insertComment)
                for (let i=0; i< response.replies.length; i++) {
                    const insertReply = document.createElement("p")
                    insertReply.innerText = `${response.user_replies[i]}: ${response.replies[i]}`
                    discussionThread.appendChild(insertReply)
                }
                const insertReply = document.createElement("form")
                const reply = document.createElement("input")
                reply.setAttribute("type", "textarea")
                reply.setAttribute("name", "reply")
                reply.setAttribute("placeholder", "Add a Reply")
                reply.setAttribute("class", "resize-textarea")
                const submit = document.createElement("button");
                submit.setAttribute("type", "submit");
                submit.innerText = "Submit"
                insertReply.appendChild(reply)
                insertReply.appendChild(submit)
                discussionThread.append(insertReply)
                submit.addEventListener("click", (evt) => {
                    evt.preventDefault()
                    fetch(`/add-reply?reply=${reply.value}`)
                    .then(response => response.json())
                    .then (replyResponse => {
                        if (replyResponse.success) {
                            const newReply = document.createElement("p")
                            newReply.innerHTML = `${replyResponse.user_reply}: ${replyResponse.reply}`
                            discussionThread.insertBefore(newReply, insertReply)
                            reply.value = ""
                        }
                    })
                })
            }
        })
    })
}

document.querySelector("#update-status").addEventListener("click", (evt) => {
    evt.preventDefault();

    const updatedStatus = document.querySelector("#updated-status").value;

    fetch(`/update-status?updated-status=${updatedStatus}`)
        .then(response => response.json())
        .then(response => {
            const updateMyStatus = document.querySelector(".update-my-status");
            removeAllChildNodes(updateMyStatus)
            updateMyStatus.innerText = response.message;
        })
})

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}