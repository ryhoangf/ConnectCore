// Toggle accordion sections
$('.title').on('click', function () {
    $('.box').slideUp(500);

    var findElm = $(this).next(".box");

    if ($(this).hasClass('close')) {
        $(this).removeClass('close');
    } else {
        $('.close').removeClass('close');
        $(this).addClass('close');
        $(findElm).slideDown(500);
    }
});

// Open accordion section if open class is present on page load
$(window).on('load', function () {
    $('.accordion-area li:first-of-type section').addClass("open");
    $(".open").each(function (index, element) {
        var Title = $(element).children('.title');
        $(Title).addClass('close');
        var Box = $(element).children('.box');
        $(Box).slideDown(500);
    });
});

// Edit button event listener to show hidden sections
document.querySelectorAll('.edit_button').forEach(function(button) {
    button.addEventListener('click', function() {
        var hiddenSection = this.closest('.box').querySelector('.hidden_section');
        hiddenSection.classList.toggle('username_hidden');
    });
});

// Handle the form submission when the "renewal_username_button" is clicked
document.querySelectorAll('.renewal_username_button').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default form submission

        var inputField = this.previousElementSibling;

        if (inputField.value.trim() !== "") {
            // Optional: Show a modal for confirmation
            var modal = document.getElementById('modal');
            modal.style.display = "block";

            // Submit the form via AJAX or simply submit it if you want to reload
            this.closest('form').submit(); // Submits the form containing the username field
        } else {
            alert("Please enter a value before submitting.");
        }
    });
});

// Close the modal window
document.querySelector('.close_button').addEventListener('click', function() {
    var modal = document.getElementById('modal');
    modal.style.display = "none";
});

// Close the modal window when clicking outside of it
window.addEventListener('click', function(event) {
    var modal = document.getElementById('modal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
});
