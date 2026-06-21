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
const csrftoken = getCookie('csrftoken');

console.log("JS loaded");

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const formData = new FormData(form);

        fetch("/settings/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            console.log(data.status);

            document.querySelector('.bio').textContent = data.bio;
            document.querySelector('.profilePicture').src = data.image_url;
            document.getElementById('bannerPicture').src = data.banner_url;
        });
    });
});