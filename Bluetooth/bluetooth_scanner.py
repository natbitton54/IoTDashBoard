import asyncio
from bleak import BleakScanner


async def scan_ble_async(threshold=-90):
    print("[BLE] Scanning for BLE devices (MAC only)...")

    devices = await BleakScanner.discover(timeout=5.0)
    filtered_devices = []

    for device in devices:
        rssi = device.rssi
        address = device.address.upper()

        print(f"[BLE] {address} - RSSI: {rssi} dBm")

        if rssi >= threshold:
            filtered_devices.append(
                {
                    "address": address,
                    "name": address,  # Use MAC as 'name'
                    "rssi": rssi,
                    "type": "BLE",
                }
            )

    return filtered_devices


def scan_ble(threshold=-90):
    try:
        return asyncio.run(scan_ble_async(threshold))
    except Exception as e:
        print(f"[BLE] Scan failed: {e}")
        return []
