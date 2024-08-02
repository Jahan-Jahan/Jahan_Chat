document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll(".card");
    cards.forEach(function(card) {
        card.addEventListener("click", function() {
            const baseUrl = cards.dataset.directMessageUrl;
            window.location.href = baseUrl;
        });
    });
});