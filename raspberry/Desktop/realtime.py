import pandas as pd
import numpy as np
import Adafruit_DHT
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# Configuración del sensor DHT11
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4 # Pin GPIO conectado al sensor DHT11

# Configuración inicial de las listas para almacenar los datos
humidity_data = []
temperature_data = []
soil_moisture_data = []

# Configuración de la gráfica en tiempo real
plt.ion()
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

def update_plot(frame):
    dht_humidity, dht_temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if dht_humidity is not None and dht_temperature is not None:
        humidity = dht_humidity
        temperature = dht_temperature

        # Simulación de lectura del sensor de humedad del suelo
        soil_moisture = np.random.uniform(10, 30)  # Rango simulado de humedad del suelo

        # Almacenar datos
        humidity_data.append(humidity)
        temperature_data.append(temperature)
        soil_moisture_data.append(soil_moisture)

        # Limitar la longitud de los datos para mantener la gráfica actualizada
        if len(humidity_data) > 50:
            humidity_data.pop(0)
            temperature_data.pop(0)
            soil_moisture_data.pop(0)

        # Actualizar las gráficas
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax1.plot(humidity_data, label='Humedad (%)')
        ax2.plot(temperature_data, label='Temperatura (°C)')
        ax3.plot(soil_moisture_data, label='Humedad del Suelo (%)')

        ax1.legend(loc='upper right')
        ax2.legend(loc='upper right')
        ax3.legend(loc='upper right')

        ax1.set_title('Humedad del Aire')
        ax2.set_title('Temperatura del Aire')
        ax3.set_title('Humedad del Suelo')

    time.sleep(1)

ani = FuncAnimation(fig, update_plot, interval=1000)

plt.tight_layout()
plt.show()