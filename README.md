# IoTDashBoard – Final Project User Guide

## Overview
This project is a Flask-based Smart Home Dashboard built for an IoT course. It connects various sensors and devices such as LEDs, DHT11, Photoresistor, DC motor (fan), and RFID with an ESP32 and Raspberry Pi using MQTT (Mosquitto) and SQLite.

---

## PHASE 1: Flask Backend + Dashboard

### Flask Installation (if not pre-installed):
```bash
sudo apt install python3-flask
```

### Running the Project:
1. Open your IDE (e.g., VS Code).
2. Run the Flask backend script.
3. Open your browser and go to:  
   `http://127.0.0.1:5000`  
   - `127.0.0.1` = Localhost  
   - `5000` = Default Flask port

### GPIO Fix (if errors occur):
```bash
sudo apt install python3-rpi.gpio
```

---

## PHASE 2: Temperature & Email Alerts

### Setup DHT11 Library:
1. Download from: https://freenove.com/FNK0025  
2. Extract the zip file.
3. Navigate to `Libs > Python-Libs`.
4. Copy the `Freenove_DHT` folder into your project.
5. run this command to install the library: sudo python setup.py

### Emailing Setup (Install via Terminal):
```bash
sudo apt install python3-smtplib
sudo apt install python3-imaplib
# or alternatively
sudo apt install python3-secure-smtplib
```

---

## PHASE 3: Light Sensor, MQTT, and Arduino

### Install Mosquitto MQTT Broker:
```bash
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto.service
mosquitto -v  # To test the broker
```

### Arduino Setup on Raspberry Pi:
```bash
sudo apt-get install fuse libfuse-dev
```

1. Download Arduino IDE for Pi:  
   [GitHub Release - Linux_arm64_app_image.zip](https://github.com/koendv/arduino-ide-raspberrypi/releases/)

2. Unzip using:
```bash
unzip filename.zip
```

### Required Arduino Libraries:
- `WiFi.h`
- `PubSubClient.h` (by Nick O'Leary)

### Install Python MQTT Client:
```bash
sudo apt install python3-paho-mqtt
```

---

## PHASE 4: RFID + Database Integration

### Install SQLite (if needed):
```bash
sudo apt install sqlite3
```

### Arduino Library for RFID:
Install `MFRC522` by GithubCommunity from Library Manager in Arduino IDE.

---

### Bluetooth Setup (for RFID scan detection using BLE or future Bluetooth capabilities):
Run these commands on the Raspberry Pi terminal to install and activate Bluetooth services:
```bash
sudo apt install -y bluetooth bluez
sudo systemctl enable bluetooth
sudo systemctl start bluetooth
sudo systemctl status bluetooth
```

```bash
python3 -m pip install bleak --break-system-packages
sudo apt install python3-bluez
```
In order to run the bluetooth on the Dashboard, run this command in VSCode Terminal
```bash
sudo python3 backend.py
```

---

## Summary
Ensure the following are installed and configured:
- Python: Flask, RPi.GPIO, smtplib, imaplib, sqlite3, paho-mqtt
- Arduino: ESP32 board support, WiFi, PubSubClient, MFRC522 libraries
- Raspberry Pi: Mosquitto broker, Freenove DHT11 library
