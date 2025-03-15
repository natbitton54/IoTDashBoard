from flask import Flask, render_template, send_from_directory, request, jsonify # use jsonify for returning messages because we are using javascript on our project
import RPi.GPIO as GPIO
from sensors.dht11F import get_temperature, get_humidity


# initialize flask app
app = Flask(__name__, template_folder="src/Views", static_folder="src")

GPIO.cleanup()

# GPIO Configuration
LED = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

# led state like lab 2 task 2 to keep light turned on til button is pressed again
led_state = False

# get html file
@app.route('/')
def home():
   return render_template('index.html')

# get css and js file
@app.route('/CSS/<path:filename>')
def serve_css(filename):
   return send_from_directory('src/CSS', filename)

@app.route('/Scripts/<path:filename>')
def serve_js(filename):
   return send_from_directory('src/Scripts', filename)

# fucntion for switching the button on or off, turning the led for both the breadboard and on the web
@app.route('/switch', methods=['POST'])
def switch_on():
   global led_state
   data = request.get_json()
   state = data.get('state', '').upper()

   if state not in ['ON', 'OFF']:
       return jsonify({'error': 'Invalid state. Use "ON" or "OFF".'}), 400

   led_state = (state == 'ON')
   GPIO.output(LED, led_state)

   return jsonify({'message': f'LED switched {state}', 'state': state})

# API endpoint to get LED status
@app.route('/status', methods=['GET'])
def get_led_status():
   return jsonify({'state': 'ON' if led_state else 'OFF'})

# API endpoints for temperature and humidity
@app.route('/temperature', methods=['GET'])
def temperature():
    temp = get_temperature()
    if temp is not None:
        return jsonify({'temperature': temp})
    else:
        return jsonify({'error': 'Failed to read temperature.'}), 500

@app.route('/humidity', methods=['GET'])
def humidity():
    humidity = get_humidity()
    if humidity is not None:
        return jsonify({'humidity': humidity})
    else:
        return jsonify({'error': 'Failed to read humidity.'}), 500

# run flask server
if __name__ == '__main__':
   try:
       app.run(host='0.0.0.0', port=5000, debug=True)
   except KeyboardInterrupt:
       GPIO.cleanup()