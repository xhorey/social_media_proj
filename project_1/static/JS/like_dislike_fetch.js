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

                const commentSection = document.querySelector('.comment_section_toggle');

                if (!commentSection) {
                    console.error("Comments modal not found!");
                    return;
                }

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