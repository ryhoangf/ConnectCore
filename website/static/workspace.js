document.addEventListener('DOMContentLoaded', () => {
    const emojiButton = document.getElementById('emoji-button');
    const messageInput = document.getElementById('messageInput');
    const emojiContainer = document.getElementById('emoji-container');
    const teamId = "{{ team_id }}"; // Đảm bảo teamId đã được định nghĩa hoặc thay đổi giá trị nếu cần.

    // Khởi tạo picker từ emoji-mart
    const picker = new EmojiMart.Picker({
        onEmojiSelect: (emoji) => {
            messageInput.value += emoji.native; // Thêm emoji vào trường nhập liệu
        },
        theme: 'auto', // Tự động chọn theme sáng/tối
        perLine: 9, // Số emoji trên mỗi dòng
        previewPosition: 'bottom', // Vị trí của phần preview
        navPosition: 'top', // Vị trí của thanh điều hướng
    });

    // Thêm picker vào container
    emojiContainer.appendChild(picker);

    // Hiển thị hoặc ẩn picker khi click vào nút emoji
    emojiButton.addEventListener('click', () => {
        if (emojiContainer.style.display === 'block') {
            emojiContainer.style.display = 'none';
        } else {
            emojiContainer.style.display = 'block';
        }
    });

    // Ẩn picker khi click ra ngoài
    document.addEventListener('click', (event) => {
        if (!emojiContainer.contains(event.target) && event.target !== emojiButton) {
            emojiContainer.style.display = 'none';
        }
    });
});

// Xử lý form submit
document.getElementById('messageForm').addEventListener('submit', function(event) {
    event.preventDefault(); 

    const messageInput = document.getElementById('messageInput');
    const messageContent = messageInput.value;

    console.log('Submitting message:', messageContent); // Debug log

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
        console.log('Response:', response); // Debug log
        return response.json();
    })
    .then(data => {
        console.log('Data:', data); // Debug log
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
