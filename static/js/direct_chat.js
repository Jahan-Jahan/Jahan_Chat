document.addEventListener("DOMContentLoaded", function() {
    var textarea = document.getElementById("message-form");
    textarea.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            document.getElementById("message-form").submit();
        }
    });
});
