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
const csrftokenFollow = getCookie('csrftoken');

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    form.addEventListener("submit", (e) => {
        e.preventDefault(); // STOP normal reload

        const formData = new FormData(form);

        fetch("/follow/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftokenFollow
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            console.log(data.status);

            document.querySelector('.follow_button_style').textContent = data.text_button;
            document.querySelector('.followers_count').textContent = data.amount_followers;
            document.querySelector('.followers_text').textContent = data.text_marker;
        });
    });
});