// themeToggle.js with localStorage
document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    let isLightMode = localStorage.getItem('theme') === 'light';

    // Apply saved theme on load
    document.body.classList.toggle('light-mode', isLightMode);
    themeToggleBtn.textContent = isLightMode ? 'Toggle Dark Mode' : 'Toggle Light Mode';

    // Theme toggle button click event
    themeToggleBtn.addEventListener('click', () => {
        isLightMode = !isLightMode;
        document.body.classList.toggle('light-mode', isLightMode);
        themeToggleBtn.textContent = isLightMode ? 'Toggle Dark Mode' : 'Toggle Light Mode';
        localStorage.setItem('theme', isLightMode ? 'light' : 'dark');
    });
});