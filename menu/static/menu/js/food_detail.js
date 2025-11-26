let currentImageIndex = 0;
let images = [];

function initializeImageGallery(imageUrls) {
    images = imageUrls;
    currentImageIndex = 0;
}

function changeMainImage(src, index) {
    const mainImage = document.getElementById('mainImage');
    if (mainImage) {
        mainImage.src = src;
    }
    document.querySelectorAll('.thumbnail').forEach((thumb, i) => {
        thumb.classList.toggle('active', i === index);
    });
    currentImageIndex = index;
}

function openModal(index) {
    if (images.length === 0) return;
    currentImageIndex = index;
    const modalImage = document.getElementById('modalImage');
    if (modalImage) {
        modalImage.src = images[currentImageIndex];
    }
    const modal = document.getElementById('imageModal');
    if (modal) {
        modal.style.display = 'block';
    }
}

function closeModal() {
    const modal = document.getElementById('imageModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function changeSlide(direction) {
    currentImageIndex += direction;
    if (currentImageIndex >= images.length) {
        currentImageIndex = 0;
    } else if (currentImageIndex < 0) {
        currentImageIndex = images.length - 1;
    }
    const modalImage = document.getElementById('modalImage');
    if (modalImage) {
        modalImage.src = images[currentImageIndex];
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('imageModal');
    if (modal) {
        document.addEventListener('keydown', function(e) {
            if (modal.style.display === 'block') {
                if (e.key === 'Escape') {
                    closeModal();
                } else if (e.key === 'ArrowLeft') {
                    changeSlide(-1);
                } else if (e.key === 'ArrowRight') {
                    changeSlide(1);
                }
            }
        });
        
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });
    }
});
