document.addEventListener("DOMContentLoaded", function() {
    const chats = document.querySelectorAll(".chat");
    chats.forEach(function(chat) {
        chat.addEventListener("click", function() {
            const baseUrl = chat.dataset.chatUrl;
            window.location.href = baseUrl;
        });
    });

    const users = document.querySelectorAll(".user");
    users.forEach(function(user) {
        user.addEventListener("click", function() {
            const baseUrl = user.dataset.userUrl;
            window.location.href = baseUrl;
        });
    });
});
