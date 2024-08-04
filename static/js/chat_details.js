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

$(document).ready(function() {
    $('.delete-chat').click(function() {
        const chatId = $(this).data('chat-id');
        $(this).hide();
        $(`#confirm-${chatId}`).show();
    });

    $('.confirm-cancel').click(function() {
        const chatId = $(this).data('chat-id');
        $(`#confirm-${chatId}`).hide();
        $(`[data-chat-id="${chatId}"]`).show();
    });

    $('.confirm-ok').click(function() {
        const chatId = $(this).data('chat-id');

        $.ajax({
            type: 'POST',
            url: `/delete-chat/${chatId}/`,
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                if (response.success) {
                    window.location.href = response.redirect_url;
                    alert('Chat has been deleted!');
                } else {
                    alert('Failed to delete chat.');
                }
            },
            error: function() {
                alert('Error deleting chat.');
            }
        });
    });

    $(document).on('click', '.delete-button', function() {
        const messageId = $(this).data('message-id');
        const messageElement = $(`#message-${messageId}`);

        if (confirm('Are you sure you want to delete this message?')) {
            $.ajax({
                type: 'POST',
                url: '/delete-message/',
                data: {
                    'message_id': messageId,
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function(response) {
                    if (response.success) {
                        messageElement.remove();
                    } else {
                        alert('Failed to delete message.');
                    }
                },
                error: function() {
                    alert('Error deleting message.');
                }
            });
        }
    });

    $('.edit-button').click(function() {
        const messageId = $(this).data('message-id');
        $(this).hide();
        $(`.delete-button[data-message-id="${messageId}"]`).hide();
        $(`.message-body[data-message-id="${messageId}"]`).hide();
        $(`.edit-textarea[data-message-id="${messageId}"]`).show();
        $(`.save-button[data-message-id="${messageId}"]`).show();
    });

    $('.save-button').click(function() {
        const messageId = $(this).data('message-id');
        const newMessageBody = $(`.edit-textarea[data-message-id="${messageId}"]`).val();

        $.ajax({
            type: 'POST',
            url: `/edit-message/${messageId}/`,
            data: {
                'message_id': messageId,
                'new_body': newMessageBody,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                if (response.success) {
                    $(`.message-body[data-message-id="${messageId}"]`).text(newMessageBody).show();
                    $(`.edit-textarea[data-message-id="${messageId}"]`).hide();
                    $(`.save-button[data-message-id="${messageId}"]`).hide();
                    $(`.edit-button[data-message-id="${messageId}"]`).show();
                    $(`.delete-button[data-message-id="${messageId}"]`).show();
                    window.location.href = response.redirect_url;
                } else {
                    alert('Failed to update message.');
                }
            },
            error: function() {
                alert('Error updating message.');
            }
        });
    });
});

