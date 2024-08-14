document.getElementById('teamForm').addEventListener('submit', function(event) {
    const teamNameInput = document.getElementById('teamName');
    const errorMessage = document.getElementById('error-message');

    if (teamNameInput.value.trim() === '') {
        event.preventDefault();
        errorMessage.textContent = 'Team name cannot be empty!';
        errorMessage.style.display = 'block';
        teamNameInput.classList.add('input-error');
    } else {
        errorMessage.style.display = 'none';
        teamNameInput.classList.remove('input-error');
    }
});

document.getElementById('teamName').addEventListener('input', function() {
    const errorMessage = document.getElementById('error-message');
    if (this.value.trim() !== '') {
        errorMessage.style.display = 'none';
        this.classList.remove('input-error');
    }
});

document.getElementById('backButton').addEventListener('click', function() {
    window.history.back();
});
