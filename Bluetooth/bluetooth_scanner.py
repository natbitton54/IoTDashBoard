import bluetooth
import subprocess


def scan_devices(threshold=-50, duration=8):
    print("Scanning for Bluetooth devices...")
    result = subprocess.run(
        ["hcitool", "scan"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )

    nearby_devices = bluetooth.discover_devices(
        duration=duration, lookup_names=True, flush_cache=True
    )
    filtered_devices = []

    for addr, name in nearby_devices:
        try:
            rssi_output = subprocess.check_output(
                ["hcitool", "rssi", addr], stderr=subprocess.DEVNULL
            ).decode()
            rssi = int(rssi_output.strip().split()[-1])
            print(f"{name} ({addr}) - RSSI: {rssi} dBm")  # for debugging
            if rssi >= threshold:
                filtered_devices.append((addr, name, rssi))
        except Exception as e:
            print(f"Error reading RSSI for {addr}: {e}")
            continue

    return filtered_devices
