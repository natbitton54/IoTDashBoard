document.addEventListener('DOMContentLoaded', () => {
    const humidityDisplay = document.getElementById('humidityDisplay');
    const humidityFillLine = document.querySelector('.humidity-fill-line');

    function updateHumidityGauge(humidity) {
        // Clamp humidity within range (0 to 100)
        const clampedHumidity = Math.max(0, Math.min(100, humidity));
        // Map humidity (0 to 100) to percentage (0 to 1) with a minimum of 0.01
        const percentage = Math.max(0, Math.min(1, clampedHumidity / 100));
        const fillPercentage = percentage;
        const dashOffset = 314.16 - (314.16 * fillPercentage);
        console.log(`Humidity: ${clampedHumidity}, Percentage: ${percentage}, Fill Percentage: ${fillPercentage}, Dash Offset: ${dashOffset}`); // Debug log

        // Update the CSS variable for SVG fill
        document.documentElement.style.setProperty('--humidity-fill-percentage', `${fillPercentage}`);

        // Force a repaint to ensure the SVG updates
        if (humidityFillLine) {
            humidityFillLine.classList.add('update');
            setTimeout(() => humidityFillLine.classList.remove('update'), 100);
        }

        // Update humidity display
        humidityDisplay.textContent = `${clampedHumidity.toFixed(1)}%`;
    }

    // Simulation 
    setInterval(() => {
        const newHumidity = Math.random() * 100 - 50;
        updateHumidityGauge(newHumidity);
    }, 5000);
});
