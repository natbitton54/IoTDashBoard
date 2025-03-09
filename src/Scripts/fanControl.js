// fanControl.js
document.addEventListener('DOMContentLoaded', () => {
    const fanGif = document.getElementById('fanGif');
    const fanToggleBtn = document.getElementById('fanToggleBtn');
    let isFanOn = false;

    // Paths to the static image and animated GIF
    const fanStaticSrc = '../src/images/fan-static.gif'; 
    const fanAnimatedSrc = '../src/images/fan.gif';    

    // Toggle button click event
    fanToggleBtn.addEventListener('click', () => {
        isFanOn = !isFanOn;
        if (isFanOn) {
            fanGif.src = fanAnimatedSrc; // Switch to animated GIF
            fanToggleBtn.textContent = 'Turn Off';
        } else {
            fanGif.src = fanStaticSrc;   // Switch to static image (simulates pause)
            fanToggleBtn.textContent = 'Turn On';
        }
    });
});