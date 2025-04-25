function updateBluetoothStatus() {
  const rssiThreshold = parseInt(
    document.getElementById("rssiThreshold").value,
    10
  );

  fetch(`/bluetooth-status?threshold=${rssiThreshold}`)
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("deviceCount").value = data.device_count;
      console.log("Devices above threshold:", data.devices); // optional debug
    })
    .catch((err) => {
      console.error("Bluetooth fetch failed:", err);
    });
}

// Manual scan
document
  .getElementById("scanBtn")
  .addEventListener("click", updateBluetoothStatus);

// Auto scan every 3 seconds
setInterval(updateBluetoothStatus, 3000);
