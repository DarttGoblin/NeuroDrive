import time
import Adafruit_DHT
import RPi.GPIO as GPIO

# Pin configuration
LIGHT_SENSOR_PIN = 0  # ADC Channel (Requires an ADC module like MCP3008)
GAS_SENSOR_PIN = 1  # ADC Channel
DHT_PIN = 12
LED_PIN_LIGHT = 6
LED_PIN_GAS = 7

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_LIGHT, GPIO.OUT)
GPIO.setup(LED_PIN_GAS, GPIO.OUT)

# Initialize DHT sensor
DHT_SENSOR = Adafruit_DHT.DHT11

def read_adc(channel):
    # Placeholder function - Replace with actual ADC reading code
    return 50  # Example value (requires MCP3008 or similar ADC)

while True:
    time.sleep(2)

    light_level = read_adc(LIGHT_SENSOR_PIN)
    gas_level = read_adc(GAS_SENSOR_PIN)
    humidity_level, temperature_level = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    if humidity_level is None or temperature_level is None:
        print("DHT11 has failed!")
        continue

    GPIO.output(LED_PIN_LIGHT, GPIO.HIGH if light_level > 20 else GPIO.LOW)
    GPIO.output(LED_PIN_GAS, GPIO.HIGH if gas_level > 500 else GPIO.LOW)

    print("Sensor Data:")
    print(f"Light Level: {light_level}")
    print(f"Gas-Smoke Level: {gas_level}")
    print(f"Temperature: {temperature_level} °C")
    print(f"Humidity: {humidity_level} %")
