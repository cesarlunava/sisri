import pandas as pd
import numpy as np
import time
import cv2
import logging
from datetime import datetime, timedelta
import random

# Set up logging
logging.basicConfig(filename='greenhouse_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

num_days = 90
pressure = 101325

# Simulated sensor functions
def read_temperature():
    return random.uniform(15, 35)  # Simulated temperature in Celsius

def read_humidity():
    return random.uniform(30, 90)  # Simulated humidity percentage

def read_light():
    return random.uniform(0, 1000)  # Simulated lux value

def read_soil_moisture():
    return random.uniform(0, 100)  # Simulated percentage

def read_ph():
    return random.uniform(5.5, 7.5)

def read_npk():
    return [random.uniform(0, 100) for _ in range(3)]  # Simulated NPK values

def read_wind_speed():
    return random.uniform(0, 20)  # Simulated wind speed in m/s

def read_flow_rate():
    return random.uniform(0, 10)  # Simulated flow rate in L/min

def control_valve(soil_moisture, threshold=30):
    if soil_moisture < threshold:
        logging.info("Solenoid valve turned on")
        return True
    else:
        logging.info("Solenoid valve turned off")
        return False

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

def simulate_camera_capture():
    # Simulate capturing an image by creating a blank one
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img.fill(200)  # Fill with a light gray color
    return img

start_time = datetime.now()
end_time = start_time + timedelta(days=num_days)

data = []

try:
    while datetime.now() < end_time:
        # Simulated sensor readings
        temperature = read_temperature()
        humidity = read_humidity()
        solar_radiation = read_light() / 3.6
        soil_moisture = read_soil_moisture()
        ph = read_ph()
        npk = read_npk()
        wind_speed = read_wind_speed()
        flow_rate = read_flow_rate()

        eto = calculate_eto(temperature, humidity, solar_radiation, wind_speed)

        # Simulate camera capture
        frame = simulate_camera_capture()
        image_path = f"images/day_{(datetime.now() - start_time).days}.jpg"
        cv2.imwrite(image_path, frame)

        data.append({
            'timestamp': datetime.now(),
            'humidity': humidity,
            'temperature': temperature,
            'solar_radiation': solar_radiation,
            'wind_speed': wind_speed,
            'soil_moisture': soil_moisture,
            'eto': eto,
            'flow_rate': flow_rate,
            'ph': ph,
            'n': npk[0],
            'p': npk[1],
            'k': npk[2],
            'image_path': image_path,
            'valve_status': control_valve(soil_moisture)
        })

        if len(data) % 100 == 0:  # Save data every 100 entries
            pd.DataFrame(data).to_csv('greenhouse_data.csv', index=False, mode='a', header=not pd.io.common.file_exists('greenhouse_data.csv'))
            data = []

        logging.info(f"Readings: Temp={temperature:.1f}°C, Humidity={humidity:.1f}%, Soil Moisture={soil_moisture:.1f}%")

        # Simulate waiting for a minute
        time.sleep(1)  # We use 1 second instead of 60 to speed up the simulation

except KeyboardInterrupt:
    logging.info("Program interrupted by user")
except Exception as e:
    logging.error(f"An error occurred: {e}")
finally:
    if data:  # Save any remaining data
        pd.DataFrame(data).to_csv('greenhouse_data.csv', index=False, mode='a', header=not pd.io.common.file_exists('greenhouse_data.csv'))
    logging.info("Program ended")

print("Simulation completed. Check 'greenhouse_data.csv' for results and 'greenhouse_log.txt' for logs.")