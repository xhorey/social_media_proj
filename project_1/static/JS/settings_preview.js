const imageButton = document.getElementById('selectImageButton');
const imageInput = document.getElementById('selectImage');
const pfp = document.querySelector('.profilePicture'); 
const resetButton = document.getElementById('resetImageButton');
const initialIcon = pfp.src;
const bannerButton = document.getElementById('selectBannerButton');
const bannerInput = document.getElementById('selectBanner');
const banner = document.getElementById('bannerPicture');
const resetBannerButton = document.getElementById('resetBannerButton');
const initalBanner = banner.src;
const themeChange = document.getElementById('dark_button');
const html = document.documentElement;

html.dataset.theme = localStorage.getItem("theme") || "light";

if (html.dataset.theme === "light"){
    themeChange.textContent = "Dark theme"

}else{
    themeChange.textContent = "Light theme"
}



imageButton.addEventListener('click', () => {
    imageInput.click();
});

bannerButton.addEventListener('click', () => {
    bannerInput.click();
});

imageInput.addEventListener('change', function() {
    const file = this.files[0];

    if (file) {
        const objectURL = URL.createObjectURL(file);
        pfp.src = objectURL;
        pfp.onload = () => URL.revokeObjectURL(objectURL);
        resetButton.classList.remove('hidden');
        imageButton.textContent = "Change Image"

    } else{
        pfp.src = initialIcon;
        resetButton.classList.add('hidden');
        imageButton.textContent = "Add Image"
        imageInput.value = '';
    }
});

bannerInput.addEventListener('change', function() {
    const file = this.files[0];

    if (file) {
        const objectURL = URL.createObjectURL(file);
        banner.src = objectURL;
        banner.onload = () => URL.revokeObjectURL(objectURL);
        resetBannerButton.classList.remove('hidden');
        bannerButton.textContent = "Change Banner"

    } else{
        banner.src = initalBanner;
        resetBannerButton.classList.add('hidden');
        bannerButton.textContent = "Add Banner"
        bannerInput.value = '';
    }
});

resetButton.addEventListener('click', () => {
    pfp.src = initialIcon;
    resetButton.classList.add('hidden');
    imageButton.textContent = "Add Image"
    imageInput.value = '';
});

resetBannerButton.addEventListener('click', () => {
    banner.src = initalBanner;
    resetBannerButton.classList.add('hidden');
    bannerButton.textContent = "Add Banner"
    bannerInput.value = '';
});

themeChange.addEventListener('click', () => {
    if (html.dataset.theme === "dark") {
        html.dataset.theme = "light";
        localStorage.setItem("theme", "light");
        themeChange.textContent = "Dark theme"

    } else {
        html.dataset.theme = "dark";
        localStorage.setItem("theme", "dark");
        themeChange.textContent = "Light theme"
    }
});