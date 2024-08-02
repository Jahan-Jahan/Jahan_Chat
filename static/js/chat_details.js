document.addEventListener("DOMContentLoaded", function() {
    var textarea = document.getElementById("message-form");
    textarea.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            document.getElementById("message-form").submit();
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const displayTime = 5000;
    const messages = document.querySelectorAll(".messages .alert");
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s ease-out';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500)
        }, displayTime);
    });
});