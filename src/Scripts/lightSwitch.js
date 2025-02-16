const canvas = document.getElementById('lightCanvas');
const ctx = canvas.getContext('2d');
const toggleBtn = document.getElementById('toggleBtn');
let isOn = false;

// Function to draw the light bulb
function drawBulb(isOn) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.beginPath();
    ctx.arc(100, 100, 50, 0, Math.PI * 2);
    ctx.closePath();

    if (isOn) {
        //glowing effect using a radial gradient
        let gradient = ctx.createRadialGradient(100, 100, 10, 100, 100, 50);
        gradient.addColorStop(0, 'yellow');
        gradient.addColorStop(1, 'rgba(255, 255, 0, 0)');
        ctx.fillStyle = gradient;
    } else {
        ctx.fillStyle = '#ccc';
    }
    ctx.fill();
    ctx.strokeStyle = '#999';
    ctx.stroke();

    ctx.beginPath();
    ctx.rect(80, 150, 40, 50);
    ctx.fillStyle = '#666';
    ctx.fill();
    ctx.stroke();
}

// Initial drawing of the bulb in "off" state
drawBulb(isOn);

// Toggle button click event
toggleBtn.addEventListener('click', () => {
    isOn = !isOn;
    drawBulb(isOn);
    toggleBtn.textContent = isOn ? 'Turn Off' : 'Turn On';
});