function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftokenLike = getCookie('csrftoken');

document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener('click', (e) => {

        if (e.target.classList.contains('like_button')) {
            const postId = e.target.dataset.postId;

            fetch('/like-post/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftokenLike
                },
                body: JSON.stringify({
                    post_id: postId
                })
            })
            .then(res => res.json())
            .then(data => {
                console.log("Like:", data);
                const post = e.target.closest('.posts');

                post.querySelector('.like-count').textContent = data.likes;
                post.querySelector('.dislike-count').textContent = data.dislikes;
            });
        }

        if (e.target.classList.contains('dislike_button')) {
            const postId = e.target.dataset.postId;

            fetch('/dislike-post/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftokenLike
                },
                body: JSON.stringify({
                    post_id: postId
                })
            })
            .then(res => res.json())
            .then(data => {
                console.log("Dislike:", data);

                const post = e.target.closest('.posts');

                post.querySelector('.like-count').textContent = data.likes;
                post.querySelector('.dislike-count').textContent = data.dislikes;
            });
        }

        if (e.target.closest('.allComments_btn:not(.close_comments_btn)')) {

            const button = e.target.closest('.allComments_btn');
            const postId = button.dataset.postId;

            fetch('/show_comments/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftokenLike
                },
                body: JSON.stringify({
                    post_id: postId
                })
            })
            .then(res => res.json())
            .then(data => {

                console.log("Comments:", data);

                const commentSection = document.querySelector('.comment_section_toggle');
                const commentsContainer = commentSection.querySelector('.all_comments');


                if (!commentSection || !commentsContainer) {
                    console.error("Comments modal not found!");
                    return;
                }

                commentsContainer.innerHTML = "";

                if (data.comments.length === 0) {
                    commentsContainer.textContent = "No comments yet.";
                }

                data.comments.forEach(comment => {

                    const commentElement = document.createElement('div');
                    commentElement.classList.add('comment');

                    const profileImage = document.createElement('img');
                    profileImage.src = comment.profile_image;
                    profileImage.alt = "Profile picture";
                    profileImage.id = `pp_comment`;

                    const username = document.createElement('p');
                    username.textContent = "@" + comment.username;
                    username.classList.add('comment_username');

                    const commentText = document.createElement('span');
                    commentText.textContent = comment.text;
                    username.classList.add('comment_text');

                    const textBox = document.createElement('div');
                    textBox.classList.add('text_of_comment');

                    const ppLink = document.createElement('a');
                    ppLink.href = `/profile/${comment.username}`;

                    const nickLink = document.createElement('a');
                    nickLink.href = `/profile/${comment.username}`;

                    commentElement.appendChild(ppLink);
                    textBox.appendChild(nickLink);
                    textBox.appendChild(commentText);
                    commentElement.appendChild(textBox);
                    ppLink.appendChild(profileImage);
                    nickLink.appendChild(username);

                    commentsContainer.appendChild(commentElement);
                });


                commentSection.style.display = "flex";
                document.body.classList.add('modal-open');
            });
        }

        if (e.target.closest('.close_comments_btn')) {

            const commentSection = document.querySelector('.comment_section_toggle');

            if (!commentSection) return;

            commentSection.style.display = "none";
            document.body.classList.remove('modal-open');
        }
    });
});