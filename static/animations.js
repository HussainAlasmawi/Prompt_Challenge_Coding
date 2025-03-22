document.addEventListener('DOMContentLoaded', () => {
    const elements = document.querySelectorAll('.card, .btn');
    elements.forEach(el => {
        el.style.transition = "transform 0.3s";
        el.addEventListener('mouseover', () => {
            el.style.transform = "scale(1.05)";
        });
        el.addEventListener('mouseout', () => {
            el.style.transform = "scale(1)";
        });
    });
});
``
