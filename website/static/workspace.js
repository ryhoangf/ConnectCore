document.getElementById('messageForm').addEventListener('submit', function(event) {
    event.preventDefault(); 

    const messageInput = document.getElementById('messageInput');
    const messageContent = messageInput.value;

    fetch(`/workspace/${teamId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'message_content': messageContent
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
        } else {
            const chatMessages = document.getElementById('chat-messages');
            const messageElement = document.createElement('div');
            messageElement.classList.add('message');

            messageElement.innerHTML = `
                <div class="message-info">
                    <span class="message-user">${data.username}</span>
                    <span class="message-timestamp">${data.created_at}</span>
                </div>
                <div class="message-content">
                    <p>${data.content}</p>
                </div>
            `;

            chatMessages.appendChild(messageElement);
            chatMessages.scrollTop = chatMessages.scrollHeight; 

            messageInput.value = ''; 
        }
    })
    .catch(error => console.error('Error:', error));
});