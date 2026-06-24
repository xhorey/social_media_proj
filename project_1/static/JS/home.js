const html = document.documentElement;

html.dataset.theme = localStorage.getItem("theme") || "light";