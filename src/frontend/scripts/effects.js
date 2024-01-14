document.addEventListener("DOMContentLoaded", function () {
    const lightbox = document.getElementById("lightbox");
    const lightboxImage = document.querySelector(".lightbox-image");
    const lightboxTriggers = document.querySelectorAll(".lightbox-trigger");

    lightboxTriggers.forEach(trigger => {
        trigger.addEventListener("click", function () {
            const imageUrl = this.src;
            lightboxImage.src = imageUrl;
            lightbox.style.display = "flex";
        });
    });
});

function closeLightbox() {
    const lightbox = document.getElementById("lightbox");
    lightbox.style.display = "none";
}
