const canvas = document.getElementById("lightCanvas");
const ctx = canvas.getContext("2d");
let isOn = false;

const centerX = canvas.width / 2;
const centerY = canvas.height / 2 - 30;
const bulbRadius = 50;

// Function to draw the light bulb
function drawBulb(isOn) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (isOn) {
    let glow = ctx.createRadialGradient(
      centerX,
      centerY,
      10,
      centerX,
      centerY,
      80
    );
    glow.addColorStop(0, "rgba(255, 255, 150, 0.8)");
    glow.addColorStop(1, "rgba(255, 255, 0, 0)");
    ctx.fillStyle = glow;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  // Draw the lightbulb
  ctx.beginPath();
  ctx.arc(centerX, centerY, bulbRadius, 0, Math.PI * 2);
  ctx.fillStyle = isOn ? "yellow" : "#ccc";
  ctx.fill();
  ctx.strokeStyle = "#999";
  ctx.lineWidth = 3;
  ctx.stroke();

  // Filament glow
  if (isOn) {
    ctx.beginPath();
    ctx.arc(centerX, centerY, 20, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(255, 255, 200, 0.6)";
    ctx.fill();
  }

  // Draw the base centered
  const baseWidth = 40;
  const baseHeight = 50;
  const baseX = centerX - baseWidth / 2;
  const baseY = centerY + bulbRadius;

  ctx.beginPath();
  ctx.rect(baseX, baseY, baseWidth, baseHeight);
  ctx.fillStyle = "#666";
  ctx.fill();
  ctx.stroke();
}

function updateStatus() {
  fetch("/light-status")
    .then((response) => response.json())
    .then((data) => {
      isOn = data.led_state === "ON";
      drawBulb(isOn);

      const lightIntensity = data.light;
      const slider = document.getElementById("lightSlider");
      const lightText = document.getElementById("lightValue");

      slider.value = lightIntensity;
      lightText.textContent = lightIntensity;
    })
    .catch((error) => console.error("Error fetching status:", error));
}

setInterval(updateStatus, 1000);

// Initial method calling
updateStatus();
