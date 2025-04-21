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


  function getUserInfo() {
    const qrCode = document.getElementById("qrInput").value.trim().toUpperCase();
    if (qrCode) {
      fetch("/qrcode", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ uid: qrCode }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            console.log("QR Code success.");
            updateUserInfo(); 
          } else {
            alert("User not found.");
          }
        })
        .catch((err) => {
          console.error("Error:", err);
          alert("Something went wrong.");
        });
    }
  }

  setInterval(updateUserInfo, 3000);
  