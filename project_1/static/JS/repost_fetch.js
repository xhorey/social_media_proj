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
const csrftokenRepost = getCookie('csrftoken');

document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('repost_button')) {
            const postId = e.target.dataset.postId;

            fetch('/repost/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftokenRepost
                },
                body: JSON.stringify({
                    post_id: postId
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success && data.no_reposts !== undefined){
                    const post = e.target.closest('.posts');
                    if (post) {
                        const countElement = post.querySelector('.reposts_count');
                        if (countElement) {
                            countElement.textContent = data.no_reposts;
                        }
                    }
                }else{
                    console.warn(data.message);
                }

            })
            .catch(err => console.error("Error processing request:", err));
        }
    });
});