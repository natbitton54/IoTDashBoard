const canvas = document.getElementById('lightCanvas');
const ctx = canvas.getContext('2d');

const centerX = canvas.width / 2; 
const centerY = canvas.height / 2 - 30; 
const bulbRadius = 50;

function drawBulb(brightness) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    let glow = ctx.createRadialGradient(centerX, centerY, 10, centerX, centerY, 80); 
    glow.addColorStop(0, `rgba(255, 255, 150, ${brightness / 100})`);
    glow.addColorStop(1, 'rgba(255, 255, 0, 0)');
    ctx.fillStyle = glow;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.beginPath();
    ctx.arc(centerX, centerY, bulbRadius, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(255, 255, 0, ${brightness / 100})`;
    ctx.fill();
    ctx.strokeStyle = '#999';
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(centerX, centerY, bulbRadius, 0, Math.PI * 2); 
    ctx.fillStyle = `rgba(255, 255, 200, ${brightness / 120})`;
    ctx.fill();

    const baseWidth = 40;
    const baseHeight = 50;
    const baseX = centerX - baseWidth / 2;
    const baseY = centerY + bulbRadius;

    ctx.beginPath();
    ctx.rect(baseX, baseY, baseWidth, baseHeight);
    ctx.fillStyle = '#666';
    ctx.fill();
    ctx.stroke();
}

// Function to update light brightness from the end point which we received from the esp
function updateLightIntensity() {
    fetch("/light-status")  
        .then(response => response.json())
        .then(data => {
            let brightness = Math.min(100, Math.max(0, (data.light / 40.95))); 
            drawBulb(brightness);
        })
        .catch(error => console.error("Error fetching LDR value:", error));
}

// Update light eevery second
setInterval(updateLightIntensity, 1000);

updateLightIntensity();
