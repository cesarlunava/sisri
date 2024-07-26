import pandas as pd
import numpy as np
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import cv2
import logging
from datetime import datetime, timedelta
import random
import Adafruit_MCP3008  # For reading analog values

# Set up logging
logging.basicConfig(filename='greenhouse_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# GPIO setup
FLOW_SENSOR_PIN = 16
ANEMOMETER_PIN = 18
RELAY_PIN = 17
DHT_PIN = 4

# LDR setup (assuming use of MCP3008 ADC)
LDR_CHANNEL = 0  # The channel on the MCP3008 where the LDR is connected

GPIO.setmode(GPIO.BCM)
GPIO.setup(ANEMOMETER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(FLOW_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)

DHT_SENSOR = Adafruit_DHT.DHT11

# Initialize MCP3008
mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10)

wind_count = 0
flow_count = 0
wind_interval = 5
flow_interval = 5

def wind_callback(channel):
    global wind_count
    wind_count += 1

def flow_callback(channel):
    global flow_count
    flow_count += 1

GPIO.add_event_detect(ANEMOMETER_PIN, GPIO.FALLING, callback=wind_callback)
GPIO.add_event_detect(FLOW_SENSOR_PIN, GPIO.FALLING, callback=flow_callback)

num_days = 90
pressure = 101325

# Sensor reading functions
def read_dht11():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return temperature, humidity

def read_light():
    # Read the analog value from the MCP3008
    value = mcp.read_adc(LDR_CHANNEL)
    # Convert the 10-bit ADC value (0-1023) to a light percentage (0-100)
    # You may need to adjust this conversion based on your specific LDR characteristics
    light_percentage = (value / 1023) * 100
    return light_percentage

def read_soil_moisture():
    return random.uniform(0, 100)  # Simulated percentage

def read_ph():
    return random.uniform(0, 14)

def read_npk():
    return [random.uniform(0, 100) for _ in range(3)]  # Simulated NPK values

def control_valve(soil_moisture, threshold=30):
    if soil_moisture is not None and soil_moisture < threshold:
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        logging.info("Solenoid valve turned on")
    else:
        GPIO.output(RELAY_PIN, GPIO.LOW)
        logging.info("Solenoid valve turned off")

def calculate_eto(temperature, humidity, solar_radiation, wind_speed):
    slope = 4098 * (0.6108 * np.exp(17.27 * temperature / (temperature + 237.3))) / (temperature + 237.3)**2
    es = 0.6108 * np.exp(17.27 * temperature / (temperature + 237.3))
    ea = es * humidity / 100
    rho = pressure / (287 * (temperature + 273.15))
    cp = 1004
    gamma = cp * pressure / (0.622 * 2.45e6)
    ra = 208 / wind_speed
    rs = 70
    delta = slope
    G = 0
    return (0.408 * delta * (solar_radiation - G) + gamma * 900 / (temperature + 273) * wind_speed * (es - ea)) / (delta + gamma * (1 + rs / ra))

start_time = datetime.now()
end_time = start_time + timedelta(days=num_days)

data = []

try:
    while datetime.now() < end_time:
        # Sensor readings
        temperature, humidity = read_dht11()
        light = read_light()
        soil_moisture = read_soil_moisture()
        ph = read_ph()
        npk = read_npk()

        # Wind speed and flow rate calculations
        wind_count = 0
        flow_count = 0
        time.sleep(max(wind_interval, flow_interval))
        wind_speed = (wind_count / wind_interval) * 2.4
        flow_rate = (flow_count / flow_interval) * 0.1

        if all(v is not None for v in [temperature, humidity, light, wind_speed]):
            solar_radiation = light * 10  # Approximate conversion, may need adjustment
            eto = calculate_eto(temperature, humidity, solar_radiation, wind_speed)

            with cv2.VideoCapture(0) as cap:
                ret, frame = cap.read()
                if ret:
                    image_path = f"images/day_{(datetime.now() - start_time).days}.jpg"
                    cv2.imwrite(image_path, frame)
                else:
                    image_path = None
                    logging.warning("Failed to capture image")

            data.append({
                'timestamp': datetime.now(),
                'humidity': humidity,
                'temperature': temperature,
                'light': light,
                'solar_radiation': solar_radiation,
                'wind_speed': wind_speed,
                'soil_moisture': soil_moisture,
                'eto': eto,
                'flow_rate': flow_rate,
                'ph': ph,
                'n': npk[0],
                'p': npk[1],
                'k': npk[2],
                'image_path': image_path
            })

            if len(data) % 100 == 0:  # Save data every 100 entries
                pd.DataFrame(data).to_csv('greenhouse_data.csv', index=False, mode='a', header=not pd.io.common.file_exists('greenhouse_data.csv'))
                data = []

            control_valve(soil_moisture)
        else:
            logging.warning("Failed to read one or more sensors")

        time.sleep(60 - ((time.time() - start_time) % 60))  # Align to minute boundaries

except KeyboardInterrupt:
    logging.info("Program interrupted by user")
except Exception as e:
    logging.error(f"An error occurred: {e}")
finally:
    if data:  # Save any remaining data
        pd.DataFrame(data).to_csv('greenhouse_data.csv', index=False, mode='a', header=not pd.io.common.file_exists('greenhouse_data.csv'))
    GPIO.cleanup()
    logging.info("Program ended, GPIO cleaned up")

print("Monitoring completed. Check 'greenhouse_data.csv' for results and 'greenhouse_log.txt' for logs.")