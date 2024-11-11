// scripts.js

// Function to handle fade-in effect on scroll
window.addEventListener("scroll", function() {
    const cards = document.querySelectorAll('.athlete-card');
    const windowHeight = window.innerHeight;

    cards.forEach(card => {
        const cardTop = card.getBoundingClientRect().top;

        // If the card is in view (near the viewport), make it visible
        if (cardTop < windowHeight - 100) {
            card.classList.add('visible');  // Add the class to trigger the fade-in
        }
    });
});

// Optional: Trigger the fade-in effect when the page first loads
window.addEventListener("load", function() {
    document.querySelectorAll('.athlete-card').forEach(card => {
        card.classList.add('visible');  // Show the card immediately on page load
    });
});

// Initialize Intersection Observer
const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // Add 'visible' class to trigger the animation when the card is in view
            entry.target.classList.add('visible');
        } else {
            // Optionally, remove the 'visible' class when the card is out of view
            entry.target.classList.remove('visible');
        }
    });
}, {
    threshold: 0.5  // Trigger when 50% of the card is in view
});

// Select all athlete cards and observe them
const cards = document.querySelectorAll('.athlete-card');
cards.forEach(card => {
    observer.observe(card);
});
