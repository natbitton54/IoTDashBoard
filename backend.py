from flask import (
    Flask,
    render_template,
    send_from_directory,
    request,
    jsonify,
)  # use jsonify for returning messages because we are using javascript on our project
from sensors.dht11F import get_humidity, get_temperature
from emails.emailing import send_email, check_response
from motors.motor import setup_motor, run_motor
from database.user_db import get_user_by_rfid
from datetime import datetime
import RPi.GPIO as GPIO  # type: ignore
import paho.mqtt.client as mqtt  # type: ignore
import threading
import time

# initialize flask app
app = Flask(__name__, template_folder="src/Views", static_folder="src")

# GPIO Configuration
GPIO.cleanup()
time.sleep(0.5)
GPIO.setwarnings(False)
LED = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
setup_motor()


# led state like lab 2 task 2 to keep light turned on til button is pressed again
# fan state for updating the status of the fan
led_state = False
fan_state = False
email_sent = False

light_led_state = False
light_email_sent = False
previous_light_state = None
light_value = "Waiting for data"


# get html file
@app.route("/")
def home():
    return render_template("index.html")


# get css and js file
@app.route("/CSS/<path:filename>")
def serve_css(filename):
    return send_from_directory("src/CSS", filename)


@app.route("/Scripts/<path:filename>")
def serve_js(filename):
    return send_from_directory("src/Scripts", filename)


# fucntion for switching the button on or off, turning the led for both the breadboard and on the web
@app.route("/switch", methods=["POST"])
def switch_on():
    global led_state
    data = request.get_json()
    state = data.get("state", "").upper()

    if state not in ["ON", "OFF"]:
        return jsonify({"error": 'Invalid state. Use "ON" or "OFF".'}), 400

    led_state = state == "ON"
    GPIO.output(LED, led_state)

    return jsonify({"message": f"LED switched {state}", "state": state})


# API endpoint to get LED status
@app.route("/status", methods=["GET"])
def get_led_status():
    return jsonify({"state": "ON" if led_state else "OFF"})


# API endpoint to get Fan status
@app.route("/fan-status", methods=["GET"])
def get_fan_status():
    global fan_state
    return jsonify({"state": "ON" if fan_state else "OFF"})


# API endpoints for temperature and humidity
@app.route("/temperature", methods=["GET"])
def temperature():
    global email_sent
    temp = get_temperature()
    if temp is not None:
        threshold = current_user.get("temp_threshold", 22)
        if temp > threshold and not email_sent:
            send_email(temp, is_temp=True, is_light=False)
            email_sent = True
        return jsonify({"temperature": temp})
    else:
        return jsonify({"error": "Failed to read temperature."}), 500


@app.route("/humidity", methods=["GET"])
def humidity():
    humidity = get_humidity()
    if humidity is not None:
        return jsonify({"humidity": humidity})
    else:
        return jsonify({"error": "Failed to read humidity."}), 500


# API endpoint to get light intensity, led state, and if the email is sent for the light status
@app.route("/light-status", methods=["GET"])
def get_light_status():
    return jsonify(
        {
            "light": light_value,
            "led_state": "ON" if light_led_state else "OFF",
            "email_sent": light_email_sent,
        }
    )


# --- EMAIL STATUS APIs ---
@app.route("/email-status", methods=["GET"])
def email_status():
    return jsonify({"email_sent": email_sent})


@app.route("/acknowledge-email", methods=["POST"])
def acknowledge_email():
    global email_sent
    email_sent = False
    return jsonify({"status": "acknowledged"})


@app.route("/light-email-status", methods=["GET"])
def light_email_status():
    return jsonify({"email_sent": light_email_sent})


@app.route("/acknowledge-light-email", methods=["POST"])
def acknowledge_light_email():
    global light_email_sent
    light_email_sent = False
    return jsonify({"status": "acknowledged"})


# helper function
def update_fan_state(new_state):
    global fan_state
    fan_state = new_state
    print(f"Fan is: {'ON' if fan_state else 'OFF'}")
    if new_state:
        run_motor("RIGHT")
    else:
        run_motor("STOP")


current_user = {}


# rfid mqtt listener
def on_rfid_tag(client, userdata, msg):
    global email_sent
    global current_user
    uid = msg.payload.decode().strip().upper()
    print(f"[RFID] Tag received: {uid}")

    user = get_user_by_rfid(uid)
    if user:
        name = user["name"]
        temp_threshold = user["temp_threshold"]
        light_threshold = user["light_threshold"]

        print(
            f"[RFID] User '{name}' recognized. Temp: {temp_threshold}, Light: {light_threshold}"
        )

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_email(f"{name} entered at {now}", is_temp=False, is_light=False)
        current_user = user
    else:
        print("[RFID] Unrecognized Tag")


@app.route("/qrcode", methods=["POST"])
def qrcode():
    global current_user
    data = request.get_json()
    uid = data.get("uid", "").strip().upper()

    user = get_user_by_rfid(uid)
    if user:
        name = user["name"]
        temp_threshold = user["temp_threshold"]
        light_threshold = user["light_threshold"]

        print(
            f"[QR] User '{name}' recognized. Temp: {temp_threshold}, Light: {light_threshold}"
        )

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_email(f"{name} entered via QR at {now}", is_temp=False, is_light=False)
        current_user = user
        return jsonify({"success": True})
    else:
        print("[QR] Unrecognized Code")
        return jsonify({"success": False}), 404


@app.route("/user")
def get_current_user():
    return jsonify(current_user)


# this is the mqtt callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker " + str(rc))
    client.subscribe("sensor/light")
    client.subscribe("rfid/tag")


# function for turning the led on based on intensity of light, and for emailing.
def on_message(client, userdata, message):
    global light_value, light_led_state, light_email_sent, previous_light_state

    payload = message.payload.decode()
    light_value = payload
    print(f"MQTT message received -- Topic: {message.topic} | Value: {payload}")

    try:
        value = int(payload)

    except ValueError:
        print("Light Value Invalid!")
        return

    threshold = current_user.get("light_threshold", 400)
    if value < threshold:
        if previous_light_state != "LOW":
            if not light_led_state:
                GPIO.output(LED, True)
                light_led_state = True
                print("Light intensity is low -- LED turned ON")

            if not light_email_sent:
                now = datetime.now().strftime("%H:%M")
                send_email(f"The Light is on at {now}", is_temp=False, is_light=True)
                light_email_sent = True
                print("Email on lighting sent!")
            previous_light_state = "LOW"
    else:
        if previous_light_state != "NORMAL":
            if light_led_state:
                GPIO.output(LED, False)
                light_led_state = False
                print("Light intensity is fine -- LED turned OFF")
            light_email_sent = False
        previous_light_state = "NORMAL"


def email_checker():
    global fan_state
    while True:
        new_fan_state = check_response()
        if new_fan_state is not None:
            update_fan_state(new_fan_state)
        time.sleep(5)


# run flask server
if __name__ == "__main__":
    try:
        # email checker
        threading.Thread(target=email_checker, daemon=True).start()

        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        mqtt_client.message_callback_add("rfid/tag", on_rfid_tag)
        mqtt_client.connect("localhost", 1883, 60)
        mqtt_client.loop_start()

        # flask app
        app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    except KeyboardInterrupt:
        GPIO.cleanup()
