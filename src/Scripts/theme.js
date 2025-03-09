// themeToggle.js
document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    let isLightMode = false;

    // Theme toggle button click event
    themeToggleBtn.addEventListener('click', () => {
        isLightMode = !isLightMode;
        document.body.classList.toggle('light-mode', isLightMode);
        themeToggleBtn.textContent = isLightMode ? 'Toggle Dark Mode' : 'Toggle Light Mode';
    });
});