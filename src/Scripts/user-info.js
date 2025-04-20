function updateUserInfo() {
    fetch('/user')
      .then(res => res.json())
      .then(data => {
        const name = data.name;
        const tempThreshold = data.temp_threshold;
        const lightThreshold = data.light_threshold;
  
        document.getElementById("userName").textContent = name || "Unknown";
        document.getElementById("userTempThreshold").textContent = tempThreshold || "-";
        document.getElementById("userLightThreshold").textContent = lightThreshold || "-";
      });
  }
  
  setInterval(updateUserInfo, 3000);
  