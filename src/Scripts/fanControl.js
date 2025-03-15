// fanControl.js
document.addEventListener('DOMContentLoaded', () => {
    const fanGif = document.getElementById('fanGif');
    const fanStatus = document.getElementById('fanStatus');
    let isFanOn = false;

    // Paths to the static GIF and animated GIF
    const fanStaticSrc = '../src/images/fan-static.gif';
    const fanAnimatedSrc = '../src/images/fan.gif';

    // Function to update fan state and UI
    function updateFanState(newState) {
        isFanOn = newState;
        if (isFanOn) {
            fanGif.src = fanAnimatedSrc; 
            fanStatus.style.color = 'green';
            fanStatus.textContent = 'ON';
        } else {
            fanGif.src = fanStaticSrc;   
            fanStatus.style.color = 'red';
            fanStatus.textContent = 'OFF';
        }
    }

    // just for testing purposes, remove when doing backend
    setInterval(() => {
        updateFanState(!isFanOn);
    }, 5000);

    // Initial state
    updateFanState(isFanOn);
});