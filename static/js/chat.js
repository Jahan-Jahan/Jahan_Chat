document.addEventListener("DOMContentLoaded", function() {
    const chatCards = document.querySelectorAll(".card");
    const baseUrl = document.querySelector(".outer-container").dataset.chatDetailsUrl;

    chatCards.forEach(function(chatCard) {
        chatCard.addEventListener("click", function() {
            const chatId = this.dataset.chatId;
            const chatName = this.dataset.chatName;
            const url = baseUrl.replace('CHAT_NAME', chatName).replace('CHAT_ID', chatId);
            window.location.href = url;
        });
    });
});
