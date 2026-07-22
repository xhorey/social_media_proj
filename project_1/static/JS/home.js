const html = document.documentElement;

html.dataset.theme = localStorage.getItem("theme") || "light";

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftokenHome = getCookie('csrftoken');

function escapeHTML(text) {
    if (!text) return "";

    return text.replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    }[char]));
}


function hashtagsToLinks(text) {
    text = escapeHTML(text);

    return text.replace(
        /#(\w+)/g,
        '<a href="/hashtag/$1">#$1</a>'
    );
}

document.addEventListener("DOMContentLoaded", () => {

    document.addEventListener("click", (e) => {
        const button = e.target.closest(".load_more_btn");

        if (!button) return;

        const postIds = [...document.querySelectorAll(".posts")]
            .map(post => post.dataset.postId);

        fetch("/home/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftokenHome,
            },
            body: JSON.stringify({
                loaded_posts: postIds
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to load posts");
            }
            return response.json();
        })
        .then(data => {

            console.log(data);

            const posts = data.posts;

            for (const post of posts){
                const newPost = document.createElement("div");
                let repostHTML = "";
                let imageHTML = "";
                let commentsHTML = "";
                if (!post.is_owner) {
                    repostHTML = `
                        <button class="repost_button" data-post-id="${post.id}">
                            🔄 <span class="reposts_count">${post.reposts}</span>
                        </button>
                    `;
                }
                if (post.image_url) {
                    imageHTML = `
                        <div class="postImage ${post.aspect_ratio}">
                            <img src="${escapeHTML(post.image_url)}" alt="Post Image">
                        </div>
                    `;
                }
                if (post.comments && post.comments.length > 0) {

                    for (const comment of post.comments) {
                        commentsHTML += `
                            <div class="comment">
                                <a href="/profile/${encodeURIComponent(comment.username)}">
                                    <img id="pp_comment" src="${comment.profile}" alt="Profile Icon">
                                </a>

                                <div class="text_of_comment">
                                    <a href="/profile/${encodeURIComponent(comment.username)}">
                                        <p class="comment_username">@${escapeHTML(comment.username)}:</p>
                                    </a>

                                    <span class="comment_text">
                                        ${hashtagsToLinks(comment.text)}
                                    </span>
                                </div>
                            </div>
                        `;
                    }

                } else {

                    commentsHTML = `
                        <p class="no_comments">No comments yet...</p>
                    `;
                }
                newPost.classList.add("posts");
                newPost.dataset.postId = post.id;
                newPost.innerHTML = `
                    <div class="post_header">
                        <a class="user_info" href="/profile/${encodeURIComponent(post.username)}">
                            <img id="pp" src="${escapeHTML(post.profile)}" alt="Profile Icon">
                            <h2 class="username_over_post">${escapeHTML(post.username)}</h2>
                        </a>
                        <div class="post_time">
                            <p>${new Date(post.created).toLocaleString()}</p>
                        </div>
                    </div>
                    ${imageHTML}
                    <div class="post-content">
                        <p class="text-of-post">${hashtagsToLinks(post.text)}</p>
                    </div>
                    <div class="post_interactions">
                        <button class="like_button" data-post-id="${post.id}">
                            👍 <span class="like-count">${post.likes}</span>
                        </button>
                        <button class="dislike_button" data-post-id="${post.id}">
                            👎 <span class="dislike-count">${post.dislikes}</span>
                        </button>
                        ${repostHTML}
                    </div>
                    
                    <form class="write_a_comment" name="new_comment" data-post-id="${post.id}">
                        <textarea class="my_comment" name="comment" placeholder="Let everybody know what you think"></textarea>
                        <button class="new_comment_button" type="submit">⌯⌲</button>
                    </form>
                    
                    <div class="Comments">
                        <h2 id="comment_header">Comments</h2>
                        ${commentsHTML}
                    </div>
                 `;
                const content_class = document.querySelector(".content");

                
                content_class.appendChild(newPost);
                
            }

            

        })
        .catch(error => console.error(error));
    });

});
