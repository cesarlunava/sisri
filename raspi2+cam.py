import pandas as pd
import numpy as np
import board
import busio
import adafruit_bh1750
import RPi.GPIO as GPIO
import minimalmodbus
import serial
import time
import Adafruit_DHT  
import cv2

sensor = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
sensor.serial.bytesize = 8
sensor.serial.parity = serial.PARITY_NONE
sensor.serial.stopbits = 1
sensor.serial.timeout = 1

i2c = busio.I2C(board.SCL, board.SDA)
bh1750 = adafruit_bh1750.BH1750(i2c)

FLOW_SENSOR_PIN = 16
ANEMOMETER_PIN = 18
RELAY_PIN = 17  
GPIO.setmode(GPIO.BCM)
GPIO.setup(ANEMOMETER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(FLOW_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)  

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

cap = cv2.VideoCapture(0)

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

humidity_data = []
temperature_data = []
solar_radiation_data = []
wind_speed_data = []
soil_moisture_data = []
eto_data = []
flow_rate_data = []
ph_data = []
image_paths = []

np.random.seed(42)

def read_sensor():
    try:
        ph = sensor.read_register(0, 1)
        npk = sensor.read_registers(1, 3)
        temperature = sensor.read_register(4, 1)
        humidity = sensor.read_register(5, 1)
        conductivity = sensor.read_register(6, 1)
        return ph, npk, temperature, humidity, conductivity
    except Exception as e:
        print(f"Error al leer el sensor: {e}")
        return None, None, None, None, None

def control_valve(soil_moisture, threshold=30):
    if (soil_moisture is not None) and (soil_moisture < threshold):
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        print("Válvula solenoide encendida")
    else:
        GPIO.output(RELAY_PIN, GPIO.LOW)
        print("Válvula solenoide apagada")

for day in range(num_days):
    ph, npk, temperature, humidity, conductivity = read_sensor()

    solar_radiation = bh1750.lux / 3.6  

    wind_count = 0
    time.sleep(wind_interval)
    wind_speed = (wind_count / wind_interval) * 2.4  

    flow_count = 0
    time.sleep(flow_interval)
    flow_rate = (flow_count / flow_interval) * 0.1  

    dht_humidity, dht_temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if dht_humidity is not None and dht_temperature is not None:
        humidity = dht_humidity
        temperature = dht_temperature

    if humidity is not None and temperature is not None:
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
        ETo = (0.408 * delta * (solar_radiation - G) + gamma * 900 / (temperature + 273) * wind_speed * (es - ea)) / (delta + gamma * (1 + rs / ra))

        humidity_data.append(humidity)
        temperature_data.append(temperature)
        solar_radiation_data.append(solar_radiation)
        wind_speed_data.append(wind_speed)
        soil_moisture_data.append(conductivity)  
        eto_data.append(ETo)
        flow_rate_data.append(flow_rate)
        ph_data.append(ph)

        ret, frame = cap.read()
        if ret:
            image_path = f"images/day_{day}.jpg"
            cv2.imwrite(image_path, frame)
            image_paths.append(image_path)
    
    control_valve(conductivity)  
    time.sleep(1)

data = pd.DataFrame({
    'humidity': humidity_data,
    'temperature': temperature_data,      
    'wind_speed': wind_speed_data,
    'soil_moisture': soil_moisture_data,
    'eto': eto_data,
    'flow_rate': flow_rate_data,
    'ph': ph_data,
    'image_path': image_paths
})

data.to_csv('greenhouse_data.csv', index=False)

cap.release()
GPIO.cleanup()
