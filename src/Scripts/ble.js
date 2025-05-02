document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ Bluetooth script loaded");

  const scanBtn = document.getElementById("scanBtn");
  if (scanBtn) {
    scanBtn.addEventListener("click", () => {
      console.log("🔘 Scan button clicked");
      updateBluetoothStatus();
    });
  } else {
    console.warn("⚠️ scanBtn not found");
  }

  // Optional: auto-scan every 3 seconds
  setInterval(updateBluetoothStatus, 3000);
});

function updateBluetoothStatus() {
  const thresholdInput = document.getElementById("rssiThreshold");
  const deviceCountInput = document.getElementById("deviceCount");
  const devicesList = document.getElementById("deviceList");

  if (!thresholdInput || !deviceCountInput || !devicesList) {
    console.error("❌ Bluetooth UI elements not found in DOM");
    return;
  }

  const rssiThreshold = parseInt(thresholdInput.value, 10);
  console.log("📡 Fetching BLE devices with RSSI >", rssiThreshold);

  devicesList.innerHTML = ""; // Clear list before scan

  fetch(`/bluetooth-status?threshold=${rssiThreshold}`)
    .then((res) => res.json())
    .then((data) => {
      console.log("📶 Devices found:", data.device_count);
      deviceCountInput.value = data.device_count;

      const shownAddresses = [];

      if (data.devices.length === 0) {
        showToast("No devices detected");
        return;
      }

      data.devices.forEach((device) => {
        const address = device.address || "Unknown";
        const rssi = device.rssi !== undefined ? `${device.rssi} dBm` : "N/A";

        const item = document.createElement("li");
        item.textContent = `${address} [BLE] - ${rssi}`;
        devicesList.appendChild(item);

        if (!shownAddresses.includes(address)) {
          shownAddresses.push(address);
          showToast(`📡 ${address} detected`);
        }
      });
    })
    .catch((err) => {
      console.error("❌ Bluetooth fetch failed:", err);
      showToast("Bluetooth fetch failed");
    });
}

function showToast(message) {
  console.log("🔔 Showing toast:", message);

  const toast = document.createElement("div");
  toast.className = "custom-toast";
  toast.innerText = message;
  document.body.appendChild(toast);

  setTimeout(() => toast.classList.add("show"), 100);
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 500);
  }, 3000);
}
