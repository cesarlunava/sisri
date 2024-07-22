import pandas as pd
import numpy as np
import board
import busio
import adafruit_bh1750
import RPi.GPIO as GPIO
import minimalmodbus
import serial
import time
import adafruit_dht  

# sensor RS485 (Aqur2020) en el puerto USB de la Pi
sensor = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
sensor.serial.bytesize = 8
sensor.serial.parity = serial.PARITY_NONE
sensor.serial.stopbits = 1
sensor.serial.timeout = 1

# sensor de luz BH1750
i2c = busio.I2C(board.SCL, board.SDA)
bh1750 = adafruit_bh1750.BH1750(i2c)

# anemómetro y sensor de flujo
FLOW_SENSOR_PIN = 17
ANEMOMETER_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(ANEMOMETER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(FLOW_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

DHT_SENSOR = adafruit_dht.DHT11
DHT_PIN = 4  # Pin GPIO conectado al sensor DHT11

# pulsos
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

# Parámetros del invernadero
num_days = 90
pressure = 101325

# datos
humidity_data = []
temperature_data = []
solar_radiation_data = []
wind_speed_data = []
soil_moisture_data = []
eto_data = []
flow_rate_data = []
ph_data = []

np.random.seed(42)

# leer el sensor Aqur2020
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

for day in range(num_days):
    # sensor Aqur2020
    ph, npk, temperature, humidity, conductivity = read_sensor()

    # sensor de luz
    solar_radiation = bh1750.lux / 3.6  

   
    wind_count = 0
    time.sleep(wind_interval)
    wind_speed = (wind_count / wind_interval) * 2.4  

  
    flow_count = 0
    time.sleep(flow_interval)
    flow_rate = (flow_count / flow_interval) * 0.1  

    # Leer el sensor DHT11
    dht_humidity, dht_temperature = adafruit_dht.read_retry(DHT_SENSOR, DHT_PIN)
    if dht_humidity is not None and dht_temperature is not None:
        humidity = dht_humidity
        temperature = dht_temperature

    if humidity is not None and temperature is not None:
        # Calcular evapotranspiración (ETo) - Penman-Monteith
        slope = 4098 * (0.6108 * np.exp(17.27 * temperature / (temperature + 237.3))) / (temperature + 237.3)**2
        es = 0.6108 * np.exp(17.27 * temperature / (temperature + 237.3))
        ea = es * humidity / 100
        rho = pressure / (287 * (temperature + 273.15))  # Densidad del aire 
        cp = 1004  # Calor específico del aire
        gamma = cp * pressure / (0.622 * 2.45e6)  # Constante psicrométrica 
        ra = 208 / wind_speed  # Resistencia aerodinámica 
        rs = 70  # Resistencia superficial 
        delta = slope
        G = 0  # Flujo de calor del suelo 
        ETo = (0.408 * delta * (solar_radiation - G) + gamma * 900 / (temperature + 273) * wind_speed * (es - ea)) / (delta + gamma * (1 + rs / ra))

        # Almacenar datos
        humidity_data.append(humidity)
        temperature_data.append(temperature)
        solar_radiation_data.append(solar_radiation)
        wind_speed_data.append(wind_speed)
        soil_moisture_data.append(conductivity)  
        eto_data.append(ETo)
        flow_rate_data.append(flow_rate)
        ph_data.append(ph)

    
    time.sleep(1)

data = pd.DataFrame({
    'humidity': humidity_data,
    'temperature': temperature_data,
    'solar_radiation': solar_radiation_data,
    'wind_speed': wind_speed_data,
    'soil_moisture': soil_moisture_data,
    'eto': eto_data,
    'flow_rate': flow_rate_data,
    'ph': ph_data
})

# Guardar los datos en un archivo CSV
data.to_csv('greenhouse_data.csv', index=False)

# Limpiar GPIO
GPIO.cleanup()