import pandas as pd
import numpy as np
import time
import logging
from datetime import datetime, timedelta
import random
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexión con la base de datos MySQL en Railway
DATABASE_URL = ""

# Crear motor de conexión
engine = create_engine(DATABASE_URL)

# Declarar la clase base
Base = declarative_base()

# Definir el modelo de datos
class GreenhouseData(Base):
    _tablename_ = 'greenhouse_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now)
    humidity = Column(Float)
    temperature = Column(Float)
    solar_radiation = Column(Float)
    wind_speed = Column(Float)
    soil_moisture = Column(Float)
    eto = Column(Float)
    flow_rate = Column(Float)
    ph = Column(Float)
    n = Column(Float)
    p = Column(Float)
    k = Column(Float)
    valve_status = Column(String)

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear sesión para interacción con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Configuración de logs
logging.basicConfig(filename='greenhouse_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Parámetros de simulación
num_days = 90
pressure = 101325

# Funciones simuladas de sensores
def read_temperature():
    return random.uniform(15, 35)

def read_humidity():
    return random.uniform(30, 90)

def read_light():
    return random.uniform(0, 1000)

def read_soil_moisture():
    return random.uniform(0, 100)

def read_ph():
    return random.uniform(5.5, 7.5)

def read_npk():
    return [random.uniform(0, 100) for _ in range(3)]

def read_wind_speed():
    return random.uniform(0, 20)

def read_flow_rate():
    return random.uniform(0, 10)

def control_valve(soil_moisture, threshold=30):
    return "on" if soil_moisture < threshold else "off"

def calculate_eto(temperature, humidity, solar_radiation, wind_speed):
    slope = 4098 * (0.6108 * np.exp(17.27 * temperature / (temperature + 237.3))) / (temperature + 237.3)**2
    es = 0.6108 * np.exp(17.27 * temperature / (temperature + 237.3))
    ea = es * humidity / 100
    rho = pressure / (287 * (temperature + 273.15))
    cp = 1004
    gamma = cp * pressure / (0.622 * 2.45e6)
    ra = 208 / wind_speed if wind_speed > 0 else 1
    rs = 70
    G = 0
    return (0.408 * slope * (solar_radiation - G) + gamma * 900 / (temperature + 273) * wind_speed * (es - ea)) / (slope + gamma * (1 + rs / ra))

# Simulación
start_time = datetime.now()
end_time = start_time + timedelta(days=num_days)

try:
    while datetime.now() < end_time:
        # Leer datos simulados
        temperature = read_temperature()
        humidity = read_humidity()
        solar_radiation = read_light() / 3.6
        soil_moisture = read_soil_moisture()
        ph = read_ph()
        npk = read_npk()
        wind_speed = read_wind_speed()
        flow_rate = read_flow_rate()
        eto = calculate_eto(temperature, humidity, solar_radiation, wind_speed)

        # Crear un registro para insertar
        data_entry = GreenhouseData(
            humidity=humidity,
            temperature=temperature,
            solar_radiation=solar_radiation,
            wind_speed=wind_speed,
            soil_moisture=soil_moisture,
            eto=eto,
            flow_rate=flow_rate,
            ph=ph,
            n=npk[0],
            p=npk[1],
            k=npk[2],
            valve_status=control_valve(soil_moisture)
        )

        # Guardar en la base de datos
        session.add(data_entry)
        session.commit()

        logging.info(f"Readings: Temp={temperature:.1f}°C, Humidity={humidity:.1f}%, Soil Moisture={soil_moisture:.1f}%")

        # Esperar 1 minuto antes de la próxima iteración
        time.sleep(60)

except KeyboardInterrupt:
    logging.info("Program interrupted by user")
except Exception as e:
    logging.error(f"An error occurred: {e}")
    session.rollback()
finally:
    session.close()
    logging.info("Program ended")

print("Simulación completada. Datos almacenados en Railway y logs en 'greenhouse_log.txt'.")