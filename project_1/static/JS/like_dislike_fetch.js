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
const csrftoken = getCookie('csrftoken');

document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener('click', (e) => {

        if (e.target.classList.contains('like_button')) {
            const postId = e.target.dataset.postId;

            fetch('/like-post/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
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
                    "X-CSRFToken": csrftoken
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

    });
});