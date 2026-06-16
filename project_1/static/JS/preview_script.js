const selectImageInput = document.getElementById('selectImage');
const aspectSelect = document.getElementById('aspect_ratio');
const previewContainer = document.getElementById('imagePreviewContainer');
const previewImg = document.getElementById('imagePreview');
const imageInput = document.getElementById('selectImage');
const imageButton = document.getElementById('selectImageButton');
const divSelector = document.querySelector('.ratio-selector'); 
const deleteImgButton = document.getElementById('deleteImageButton');


imageButton.addEventListener('click', () => {
    imageInput.click();
});

deleteImgButton.addEventListener('click', () => {
    imageInput.value = '';
    previewContainer.style.display = 'none';
    previewImg.src = '';
    divSelector.classList.add('hidden');
    deleteImgButton.classList.add('hidden');
    imageButton.textContent = "Add Image"
});

selectImageInput.addEventListener('change', function() {
    const file = this.files[0];

    if (file) {
        const objectURL = URL.createObjectURL(file);
        previewImg.src = objectURL;
        previewContainer.style.display = 'block';
        previewImg.onload = () => URL.revokeObjectURL(objectURL);
        divSelector.classList.remove('hidden');
        deleteImgButton.classList.remove('hidden');
        imageButton.textContent = "Change Image"

    } else{
        previewContainer.style.display = 'none';
        previewImg.src = '';
        divSelector.classList.add('hidden');
        deleteImgButton.classList.add('hidden');
        imageButton.textContent = "Add Image"
    }
});

aspectSelect.addEventListener('change', function() {
    previewContainer.classList.remove('landscape', 'square', 'portrait');
    previewContainer.classList.add(this.value);
});