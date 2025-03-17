import RPi.GPIO as GPIO #type: ignore

MOTOR_IN1 = 27
MOTOR_IN2 = 17
MOTOR_ENABLE = 22

# setup
def setup_motor():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTOR_IN1, GPIO.OUT)
    GPIO.setup(MOTOR_IN2, GPIO.OUT)
    GPIO.setup(MOTOR_ENABLE, GPIO.OUT)

    GPIO.output(MOTOR_IN1, GPIO.LOW)
    GPIO.output(MOTOR_IN2, GPIO.LOW)
    GPIO.output(MOTOR_ENABLE, GPIO.LOW)

# function to control motor
def run_motor(direction):
    if direction == "RIGHT":
        GPIO.output(MOTOR_ENABLE, GPIO.HIGH)
        GPIO.output(MOTOR_IN1, GPIO.HIGH)
        GPIO.output(MOTOR_IN2, GPIO.LOW)
        print("Motor running RIGHT")
    elif direction == "LEFT":
        GPIO.output(MOTOR_ENABLE, GPIO.HIGH)
        GPIO.output(MOTOR_IN1, GPIO.LOW)
        GPIO.output(MOTOR_IN2, GPIO.HIGH)
        print("Motor running LEFT")
    elif direction == "STOP":
        GPIO.output(MOTOR_ENABLE, GPIO.LOW)
        GPIO.output(MOTOR_IN1, GPIO.LOW)
        GPIO.output(MOTOR_IN2, GPIO.LOW)
        print("Motor STOPPED")