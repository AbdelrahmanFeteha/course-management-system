// Add JavaScript for interactive elements if needed
document.addEventListener('DOMContentLoaded', () => {
    // Example: Fade out alert messages after 3 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = 0;
        }, 3000);
    });
});
