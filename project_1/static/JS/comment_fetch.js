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
const csrftokenComment = getCookie('csrftoken');

document.addEventListener("DOMContentLoaded", () => {
    const commentForms = document.querySelectorAll(".write_a_comment");

    commentForms.forEach(form => {
        form.addEventListener("submit", (e) => {
            e.preventDefault();

            const formData = new FormData(form);

            const postId = form.dataset.postId;
            formData.append("post_id", postId);

            fetch("/comment/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftokenComment
                },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                console.log(data.status);

                form.querySelector(".my_comment").value = "";

                const commentsContainer = form.closest(".posts").querySelector(".Comments");
    
                const noComments = commentsContainer.querySelector(".no_comments");
                if (noComments) {
                    noComments.remove();
                }

                const newComment = document.createElement("div");
                newComment.classList.add("comment");

                 newComment.innerHTML = `
                    <a href="/profile/${data.username}">
                        <img id="pp_comment" src="${data.profile_img}" alt="Profile Icon">
                    </a>

                    <div class="text_of_comment">
                        <a href="/profile/${data.username}">
                            <p class="comment_username">@${data.username}:</p>
                        </a>
                        ${formData.get("comment")}
                    </div>
                 `;

                const firstComment = commentsContainer.querySelector(".comment");

                if (firstComment) {
                    commentsContainer.insertBefore(newComment, firstComment);
                } else {
                    commentsContainer.appendChild(newComment);
                }

            });
        });
    });
});