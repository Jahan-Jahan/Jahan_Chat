document.addEventListener("DOMContentLoaded", function() {
    const addFriendBtn = document.querySelector(".btn.add-friend");
    if (addFriendBtn) {
        const baseUrl = addFriendBtn.dataset.addFriendUrl;
        addFriendBtn.addEventListener("click", function() {
            window.location.href = baseUrl;
        });
    }
});
