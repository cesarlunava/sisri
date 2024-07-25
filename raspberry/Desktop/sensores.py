import RPi.GPIO as GPIO
import time

# Configuración del pin GPIO
pin_sensor = 17  # Ejemplo de pin GPIO, ajusta según tu conexión física

def setup():
    GPIO.setmode(GPIO.BCM)  # Configura el modo de numeración de pines GPIO
    GPIO.setup(pin_sensor, GPIO.IN)  # Configura el pin como entrada

def read_soil_humidity():
    # Leer valor digital del pin
    humidity_digital = GPIO.input(pin_sensor)
    return humidity_digital

if __name__ == '__main__':
    try:
        setup()
        while True:
            soil_humidity = read_soil_humidity()
            print(f"Humedad del suelo (digital): {soil_humidity}")
            time.sleep(1)  # Espera 1 segundo antes de la próxima lectura

    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario")
    finally:
        GPIO.cleanup()  # Limpia la configuración de los pines GPIO al salir del programa