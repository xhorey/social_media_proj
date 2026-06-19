const imageButton = document.getElementById('selectImageButton');
const imageInput = document.getElementById('selectImage');
const pfp = document.querySelector('.profilePicture'); 
const resetButton = document.getElementById('resetImageButton');
const initialIcon = pfp.src;

imageButton.addEventListener('click', () => {
    imageInput.click();
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
    }
});

resetButton.addEventListener('click', () => {
    pfp.src = initialIcon;
    resetButton.classList.add('hidden');
    imageButton.textContent = "Add Image"
});