// script.js
document.addEventListener('DOMContentLoaded', () => {
    const tempDisplay = document.getElementById('tempDisplay');
    const ticksContainer = document.querySelector('.gauge-ticks');
    const labelsContainer = document.querySelector('.gauge-labels');

    // Initial temperature
    let currentTemp = 0;

    // Generate tick marks and labels
    const minTemp = -50;
    const maxTemp = 50;
    const tempRange = maxTemp - minTemp; // 100
    const numTicks = 9; // increments of 12.5

    for (let i = 0; i < numTicks; i++) {
        const temp = minTemp + (i * (tempRange / (numTicks - 1)));
        const angle = (i / (numTicks - 1)) * 360; // Full circle

        // Tick mark
        const tick = document.createElement('div');
        tick.className = 'tick';
        tick.style.setProperty('--angle', `${angle}deg`);
        ticksContainer.appendChild(tick);

        // Label (only for -50°C, 0°C, 50°C)
        const tempLabel = document.createElement('div');
        if (temp === 50 || temp === 0) {
            tempLabel.className = 'tempLabel';
            tempLabel.textContent = temp === 0 ? `${temp}` : `±${temp}°C`;
            tempLabel.style.marginLeft = temp === 0 ? "0px" : "14px";
            const rad = angle * (Math.PI / 180);
            const radius = 130; // Distance from center
            const x = 125 + radius * Math.cos(rad); // 125 is half of 250px
            const y = 125 + radius * Math.sin(rad);
            tempLabel.style.left = `${x}px`;
            tempLabel.style.top = `${y}px`;
            labelsContainer.appendChild(tempLabel);
        }
    }

function fetchTemperature() {
    fetch('/temperature')  
        .then(response => response.json())
        .then(data => {
            if (data.temperature) {
                currentTemp = data.temperature; 
                updateGauge(currentTemp);
            } else {
                console.error('Failed to fetch temperature.');
            }
        })
        .catch(error => {
            console.error('Error fetching temperature:', error);
        });
}

// Update the temperature gauge
function updateGauge(temp) {
    const percentage = (temp - minTemp) / (maxTemp - minTemp);
    const fillPercentage = percentage;
    document.documentElement.style.setProperty('--fill-percentage', `${fillPercentage}`);
    tempDisplay.textContent = `${temp.toFixed(1)}°C`;
}

updateGauge(currentTemp);

// Fetch temperature every 3 seconds
setInterval(fetchTemperature, 3000);
});
