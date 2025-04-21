let isOn = false;

function drawBulb(isOn) {
  const bulbImg = document.getElementById("lightBulbImg");
  const stateText = document.getElementById("bulbState");

  if (bulbImg) {
    bulbImg.src = isOn
      ? "https://www.w3schools.com/js/pic_bulbon.gif"
      : "https://www.w3schools.com/js/pic_bulboff.gif";
  }

  if (stateText) {
    stateText.textContent = isOn ? "ON" : "OFF";
    stateText.style.color = "red";
  }
}

function updateStatus() {
  fetch("/light-status")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      const lightIntensity = data.light;
      const slider = document.getElementById("lightSlider");
      const lightText = document.getElementById("lightValue");

      isOn = data.led_state === "ON";
      drawBulb(isOn);

      if (!isNaN(lightIntensity)) {
        slider.value = lightIntensity;
        lightText.textContent = `Brightness: ${lightIntensity}%`;
        const percentage = (lightIntensity / 4095) * 100;
        slider.style.background = `linear-gradient(to right, var(--link-hover-color) 0%, var(--link-hover-color) ${percentage}%, #aaa ${percentage}%, #aaa 100%)`;
      } else {
        throw new Error("Received NaN value for light intensity");
      }
    })
    .catch((error) => {
      console.error("Error fetching status:", error);
      const lightText = document.getElementById("lightValue");
      lightText.textContent = "Brightness: Unable to fetch data";
      drawBulb(false);
    })
    .finally(() => {
      // Schedule the next update after the current one finishes
      setTimeout(updateStatus, 1000);
    });
}

// Initial call to start the update loop
updateStatus();
