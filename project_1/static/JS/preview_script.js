const selectImageInput = document.getElementById('selectImage');
const aspectSelect = document.getElementById('aspect_ratio');
const previewContainer = document.getElementById('imagePreviewContainer');
const previewImg = document.getElementById('imagePreview');

selectImageInput.addEventListener('change', function() {
    const file = this.files[0];

    if (file) {
        const objectURL = URL.createObjectURL(file);
        previewImg.src = objectURL;
        previewContainer.style.display = 'block';
        previewImg.onload = () => URL.revokeObjectURL(objectURL);
    } else{
        previewContainer.style.display = 'none';
        previewImg.src = '';
    }
});

aspectSelect.addEventListener('change', function() {
    previewContainer.classList.remove('landscape', 'square', 'portrait');
    previewContainer.classList.add(this.value);
});