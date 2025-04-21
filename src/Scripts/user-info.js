function updateUserInfo() {
  fetch("/user")
    .then((res) => res.json())
    .then((data) => {
      const name = data.name;
      const tempThreshold = data.temp_threshold;
      const lightThreshold = data.light_threshold;
      const pfpURL = data.pfp_url;

      document.getElementById("userName").textContent = name || "Unknown";
      document.getElementById("userTempThreshold").textContent =
        tempThreshold || "-";
      document.getElementById("userLightThreshold").textContent =
        lightThreshold || "-";

      const pfpContainer = document.querySelector(".pfp");
      if (pfpContainer) {
        if (pfpURL) {
          pfpContainer.innerHTML = `
            <img src="${pfpURL}" alt="Profile Picture"
                 style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover;"
                 onerror="this.parentNode.innerHTML='<i class=\\'fa-solid fa-user\\'></i>';">
          `;
        } else {
          pfpContainer.innerHTML = '<i class="fa-solid fa-user"></i>';
        }
      }
    })
    .catch((err) => {
      console.error("Failed to fetch user info:", err);
      Swal.fire({
        icon: "error",
        title: "Oops!",
        text: "Unable to load user info from the server.",
      });
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
          localStorage.setItem("uid", qrCode);
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

window.addEventListener("DOMContentLoaded", () => {
  const savedUID = localStorage.getItem("uid");
  if (savedUID) {
    fetch("/qrcode", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ uid: savedUID }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          console.log("Auto-login with stored UID");
          updateUserInfo();
        } else {
          console.warn("Stored UID invalid. Clearing localStorage.");
          localStorage.removeItem("uid");
        }
      })
      .catch((err) => {
        console.warn("Auto-login failed.");
        console.error(err);
      });
  }
});
