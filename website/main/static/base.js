document.addEventListener('DOMContentLoaded', function () {
    const alertCloseButtons = document.querySelectorAll('.alert .btn-close');
    alertCloseButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const alert = this.closest('.alert');
            alert.style.display = 'none';
        });
    });
});
