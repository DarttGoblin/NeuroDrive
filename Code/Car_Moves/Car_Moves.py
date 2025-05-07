import RPi.GPIO as GPIO
import time
import random

class Servo:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 50)
        self.pwm.start(0)

    def write(self, angle):
        duty = angle / 18 + 2.5
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.3)  

class SmartCar:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Motor 1 pins
        self.motor1_A1 = 23
        self.motor1_A2 = 22
        self.motor1_B1 = 27
        self.motor1_B2 = 17

        # Motor 2 pins
        self.motor2_A1 = 14
        self.motor2_A2 = 4
        self.motor2_B1 = 3
        self.motor2_B2 = 2

        # LED pins
        self.front_right_yellow = 18
        self.front_left_yellow = 15
        self.back_right_yellow = 24
        self.back_left_yellow = 10
        self.red = 25

        # Object Avoidance pins
        self.echo_pin = 9
        self.trig_pin = 11
        self.servo_pin = 8
        self.buzzer_pin = 7
        self.green_led_pin = 5

        # Initialize servo and distance variables
        self.servo = Servo(self.servo_pin)
        self.allowed_distance = 50
        self.distance = 0
        self.left_distance = 0
        self.right_distance = 0

        # Setup all pins
        self._setup_pins()

    def _setup_pins(self):
        # Motor pins
        motor1_pins = [self.motor1_A1, self.motor1_A2, self.motor1_B1, self.motor1_B2]
        motor2_pins = [self.motor2_A1, self.motor2_A2, self.motor2_B1, self.motor2_B2]
        led_pins = [
            self.front_right_yellow, self.back_right_yellow,
            self.front_left_yellow, self.back_left_yellow, self.red
        ]

        # Set all motor and LED pins as output
        for pin in motor1_pins + motor2_pins + led_pins:
            GPIO.setup(pin, GPIO.OUT)

        # Set up object avoidance pins
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        GPIO.setup(self.green_led_pin, GPIO.OUT)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def _reset_lights(self):
        GPIO.output(self.front_right_yellow, GPIO.LOW)
        GPIO.output(self.back_right_yellow, GPIO.LOW)
        GPIO.output(self.front_left_yellow, GPIO.LOW)
        GPIO.output(self.back_left_yellow, GPIO.LOW)
        GPIO.output(self.green_led_pin, GPIO.LOW)
        GPIO.output(self.red, GPIO.LOW)

    def horn(self):
        print('Horning')
        time.sleep(0.4)
        GPIO.output(self.buzzer_pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.buzzer_pin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.buzzer_pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.buzzer_pin, GPIO.LOW)

    def forward(self):
        self._reset_lights()

        GPIO.output(self.motor1_A1, GPIO.HIGH)
        GPIO.output(self.motor1_A2, GPIO.LOW)
        GPIO.output(self.motor1_B1, GPIO.HIGH)
        GPIO.output(self.motor1_B2, GPIO.LOW)

        GPIO.output(self.motor2_A1, GPIO.LOW)
        GPIO.output(self.motor2_A2, GPIO.HIGH)
        GPIO.output(self.motor2_B1, GPIO.LOW)
        GPIO.output(self.motor2_B2, GPIO.HIGH)

    def backward(self):
        print('Going backward')
        self._reset_lights()
        GPIO.output(self.red, GPIO.HIGH)

        GPIO.output(self.motor1_A1, GPIO.LOW)
        GPIO.output(self.motor1_A2, GPIO.HIGH)
        GPIO.output(self.motor1_B1, GPIO.LOW)
        GPIO.output(self.motor1_B2, GPIO.HIGH)

        GPIO.output(self.motor2_A1, GPIO.HIGH)
        GPIO.output(self.motor2_A2, GPIO.LOW)
        GPIO.output(self.motor2_B1, GPIO.HIGH)
        GPIO.output(self.motor2_B2, GPIO.LOW)

    def turn_left(self):
        print('Turning left')
        self._reset_lights()
        GPIO.output(self.front_left_yellow, GPIO.HIGH)
        GPIO.output(self.back_left_yellow, GPIO.HIGH)

        GPIO.output(self.motor1_A1, GPIO.LOW)
        GPIO.output(self.motor1_A2, GPIO.HIGH)
        GPIO.output(self.motor1_B1, GPIO.HIGH)
        GPIO.output(self.motor1_B2, GPIO.LOW)

        GPIO.output(self.motor2_A1, GPIO.HIGH)
        GPIO.output(self.motor2_A2, GPIO.LOW)
        GPIO.output(self.motor2_B1, GPIO.HIGH)
        GPIO.output(self.motor2_B2, GPIO.LOW)

    def turn_right(self):
        print('Turning right')
        self._reset_lights()
        GPIO.output(self.front_right_yellow, GPIO.HIGH)
        GPIO.output(self.back_right_yellow, GPIO.HIGH)

        GPIO.output(self.motor1_A1, GPIO.HIGH)
        GPIO.output(self.motor1_A2, GPIO.LOW)
        GPIO.output(self.motor1_B1, GPIO.LOW)
        GPIO.output(self.motor1_B2, GPIO.HIGH)

        GPIO.output(self.motor2_A1, GPIO.LOW)
        GPIO.output(self.motor2_A2, GPIO.HIGH)
        GPIO.output(self.motor2_B1, GPIO.HIGH)
        GPIO.output(self.motor2_B2, GPIO.LOW)

    def stop(self):
        print('Stopping')
        self._reset_lights()
        GPIO.output(self.red, GPIO.HIGH)

        motor1_pins = [self.motor1_A1, self.motor1_A2, self.motor1_B1, self.motor1_B2]
        motor2_pins = [self.motor2_A1, self.motor2_A2, self.motor2_B1, self.motor2_B2]

        for pin in motor1_pins + motor2_pins:
            GPIO.output(pin, GPIO.LOW)

    def measure_distance(self):
        """Measure distance using the ultrasonic sensor."""
        GPIO.output(self.trig_pin, GPIO.LOW)
        time.sleep(0.000002)  # 2 microseconds
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(0.00001)   # 10 microseconds
        GPIO.output(self.trig_pin, GPIO.LOW)

        pulse_start = time.time()
        pulse_end = time.time()

        timeout_start = time.time()
        while GPIO.input(self.echo_pin) == GPIO.LOW:
            pulse_start = time.time()
            if time.time() - timeout_start > 0.1:
                return 9999

        timeout_start = time.time()
        while GPIO.input(self.echo_pin) == GPIO.HIGH:
            pulse_end = time.time()
            if time.time() - timeout_start > 0.1:
                return 9999

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        return distance

    def object_avoidance(self):
        """Main object avoidance logic."""
        self.servo.write(90)
        self.distance = self.measure_distance()
        self.forward()
        print(f"Distance: {self.distance} cm")

        if self.distance < self.allowed_distance:
            self.stop()
            GPIO.output(self.green_led_pin, GPIO.HIGH)
            self.horn()

            time.sleep(1)

            self.servo.write(180)
            time.sleep(0.2)
            self.left_distance = self.measure_distance()
            print(f"Left Distance: {self.left_distance} cm")

            self.servo.write(0)
            time.sleep(0.2)
            self.right_distance = self.measure_distance()
            print(f"Right Distance: {self.right_distance} cm")

            self.servo.write(90)
            time.sleep(0.2)

            if self.right_distance > self.allowed_distance and self.left_distance < self.allowed_distance:
                self.turn_right()
            elif self.left_distance > self.allowed_distance and self.right_distance < self.allowed_distance:
                self.turn_left()
            elif self.left_distance < self.allowed_distance and self.right_distance < self.allowed_distance:
                if random.randint(0, 1) == 0:
                    self.turn_right()
                else:
                    self.turn_left()
                time.sleep(0.2)
            else:
                if random.randint(0, 1) == 0:
                    self.turn_right()
                else:
                    self.turn_left()

            time.sleep(0.2)

        time.sleep(0.1)

    def cleanup(self):
        """Clean up GPIO settings"""
        GPIO.cleanup()

def main():
    car = SmartCar()

    try:
        print("Starting smart car with object avoidance...")
        while True:
            car.object_avoidance()
            
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    finally:
        car.cleanup()

if __name__ == "__main__":
    main()
