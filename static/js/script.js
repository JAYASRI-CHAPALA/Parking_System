// Auto-dismiss after 3 seconds
setTimeout(function () {
    const alertBox = document.getElementById('custom-alert');
    if (alertBox) {
        alertBox.style.transition = "opacity 0.5s ease";
        alertBox.style.opacity = "0";
        setTimeout(() => alertBox.remove(), 500);
    }
}, 3000);
