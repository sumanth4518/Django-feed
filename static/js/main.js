/**
 * SocialApp Main JavaScript
 * Handles image previews, toasts, micro-interactions, copy link, and form enhancements.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Bootstrap tooltips & toasts
    const toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(toastEl => {
        const toast = new bootstrap.Toast(toastEl, { delay: 5000 });
        toast.show();
    });

    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    // 2. Image Preview Handler for Create/Edit Post
    const postImageInput = document.getElementById('post-image-input');
    const previewContainer = document.getElementById('image-preview-container');
    const previewImage = document.getElementById('image-preview');
    const removePreviewBtn = document.getElementById('btn-remove-preview');

    if (postImageInput && previewContainer && previewImage) {
        postImageInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file) {
                // Check if image file
                if (!file.type.startsWith('image/')) {
                    alert('Please select a valid image file (PNG, JPG, JPEG, WEBP).');
                    this.value = '';
                    return;
                }

                // Check file size (10MB)
                if (file.size > 10 * 1024 * 1024) {
                    alert('Image file size must be less than 10MB.');
                    this.value = '';
                    return;
                }

                const reader = new FileReader();
                reader.onload = function (e) {
                    previewImage.src = e.target.result;
                    previewContainer.classList.remove('d-none');
                };
                reader.readAsDataURL(file);
            }
        });

        if (removePreviewBtn) {
            removePreviewBtn.addEventListener('click', function () {
                postImageInput.value = '';
                previewImage.src = '';
                previewContainer.classList.add('d-none');
                
                // If this is in edit mode, mark remove_image hidden input if present
                const removeImageHiddenInput = document.getElementById('id_remove_image');
                if (removeImageHiddenInput) {
                    removeImageHiddenInput.value = 'true';
                }
            });
        }
    }

    // 3. Profile Avatar Preview Handler
    const profileImageInput = document.getElementById('profile-image-input');
    const profileAvatarPreview = document.getElementById('profile-avatar-preview');

    if (profileImageInput && profileAvatarPreview) {
        profileImageInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file) {
                if (!file.type.startsWith('image/')) {
                    alert('Please select a valid image file (PNG, JPG, JPEG, WEBP).');
                    this.value = '';
                    return;
                }

                if (file.size > 5 * 1024 * 1024) {
                    alert('Profile image size must be less than 5MB.');
                    this.value = '';
                    return;
                }

                const reader = new FileReader();
                reader.onload = function (e) {
                    profileAvatarPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // 4. Copy Post Link to Clipboard
    const copyButtons = document.querySelectorAll('.btn-copy-link');
    copyButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.getAttribute('data-url');
            if (url) {
                navigator.clipboard.writeText(url).then(() => {
                    const originalHtml = this.innerHTML;
                    this.innerHTML = '<i class="bi bi-check-lg text-success"></i> Copied!';
                    setTimeout(() => {
                        this.innerHTML = originalHtml;
                    }, 2000);
                }).catch(err => {
                    console.error('Could not copy link: ', err);
                });
            }
        });
    });

    // 5. Interactive Like Button (Client-side toggle feedback)
    const likeButtons = document.querySelectorAll('.post-action-like');
    likeButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const icon = this.querySelector('i');
            const countSpan = this.querySelector('.like-count');
            let count = parseInt(countSpan ? countSpan.innerText : '0') || 0;

            if (this.classList.contains('active-like')) {
                this.classList.remove('active-like');
                icon.className = 'bi bi-heart';
                if (countSpan && count > 0) countSpan.innerText = count - 1;
            } else {
                this.classList.add('active-like');
                icon.className = 'bi bi-heart-fill text-danger';
                if (countSpan) countSpan.innerText = count + 1;
            }
        });
    });
});
