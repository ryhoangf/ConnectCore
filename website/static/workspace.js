document.addEventListener('DOMContentLoaded', () => {
    const emojiButton = document.getElementById('emoji-button');
    const messageInput = document.getElementById('messageInput');
    const emojiContainer = document.getElementById('emoji-container');
    const teamId = "{{ team_id }}"; 

    const picker = new EmojiMart.Picker({
        onEmojiSelect: (emoji) => {
            messageInput.value += emoji.native; 
        },
        theme: 'auto',
        perLine: 9, 
        previewPosition: 'bottom',
        navPosition: 'top', 
    });

    emojiContainer.appendChild(picker);

    emojiButton.addEventListener('click', () => {
        if (emojiContainer.style.display === 'block') {
            emojiContainer.style.display = 'none';
        } else {
            emojiContainer.style.display = 'block';
        }
    });

    document.addEventListener('click', (event) => {
        if (!emojiContainer.contains(event.target) && event.target !== emojiButton) {
            emojiContainer.style.display = 'none';
        }
    });
});

document.getElementById('messageForm').addEventListener('submit', function(event) {
    event.preventDefault(); 

    const messageInput = document.getElementById('messageInput');
    const messageContent = messageInput.value;

    console.log('Submitting message:', messageContent); 

    fetch(`/workspace/${teamId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'message_content': messageContent
        })
    })
    .then(response => {
        console.log('Response:', response);
        return response.json();
    })
    .then(data => {
        console.log('Data:', data); 
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
                    <p class="translatable" data-text="${data.content}">${data.content}</p>
                </div>
            `;

            chatMessages.appendChild(messageElement);
            chatMessages.scrollTop = chatMessages.scrollHeight; 

            messageInput.value = ''; 
        }
    })
    .catch(error => console.error('Error:', error));
});

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.translatable').forEach(element => {
        const translationBox = element.nextElementSibling; 

        element.addEventListener('mouseover', async () => {
            const text = element.getAttribute('data-text');
            const translatedText = await translateText(text);
            translationBox.textContent = translatedText;
            translationBox.style.display = 'block';
        });

        element.addEventListener('mouseout', () => {
            translationBox.style.display = 'none';
        });
    });

    async function translateText(text) {
        try {
            const response = await fetch('/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    text: text
                })
            });
            const data = await response.json();
            if (data.translatedText) {
                return data.translatedText;
            } else {
                console.error('Translation error:', data.error);
                return `Translation not available: ${data.error}`;
            }
        } catch (error) {
            console.error('Error fetching translation:', error);
            return 'Error occurred';
        }
    }
});
