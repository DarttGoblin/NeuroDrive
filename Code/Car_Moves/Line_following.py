import RPi.GPIO as GPIO
import time

left_sensor = 6
right_sensor = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(left_sensor, GPIO.IN)
GPIO.setup(right_sensor, GPIO.IN)

try:
    while True:
        left_sensor_state = GPIO.input(left_sensor)
        right_sensor_state = GPIO.input(right_sensor)

        if left_sensor_state == GPIO.LOW and right_sensor_state == GPIO.LOW:
            print("in line") 
        elif left_sensor_state == GPIO.LOW and right_sensor_state == GPIO.HIGH:
            print("right out line")
        elif left_sensor_state == GPIO.HIGH and right_sensor_state == GPIO.LOW:
            print("left out line")
        else:
            print("out line")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram stopped by user")
finally:
    GPIO.cleanup()
