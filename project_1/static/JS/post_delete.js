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
const csrftokenDelete = getCookie('csrftoken');

document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('answer_yes')) {
            const postId = e.target.dataset.postId;

            fetch('/delete_post/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftokenDelete
                },
                body: JSON.stringify({
                    post_id: postId
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    e.target.closest('.posts')?.remove();
                }else {
                        alert("Failed to delete post");
                    }
                })
                .catch(err => {
                    console.error(err);
                    alert("Something went wrong");
                });
        }

        if(e.target.classList.contains('delete_button')){
            const post = e.target.closest('.posts');
            const question = post.querySelector('.question_delete');
            question.classList.toggle('show');
        }
    });
});
