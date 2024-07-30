document.addEventListener("DOMContentLoaded", function() {
    var textarea = document.getElementById("message-form");
    textarea.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevent the default new line behavior
            document.getElementById("message-form").submit(); // Submit the form
        }
    });
});