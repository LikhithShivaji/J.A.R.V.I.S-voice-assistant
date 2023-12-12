import time
import pyfirmata

# Arduino board setup
board = pyfirmata.Arduino('COM3')  # Change 'COM3' to match your Arduino's port

# Configure DHT11 sensor pin
sensor_pin = board.get_pin('d:2:i')

def check_sensor():
    try:
        sensor_pin.enable_reporting()
        time.sleep(2)  # Allow time for the sensor to stabilize
        humidity = sensor_pin.read()[0]
        temperature = sensor_pin.read()[1]

        if humidity is not None and temperature is not None:
            print(f"Humidity: {humidity:.2f}%")
            print(f"Temperature: {temperature:.2f}°C")
        else:
            print("Failed to read sensor data")

    except:
        print("Error accessing the sensor")

# Main loop
while True:
    check_sensor()
    time.sleep(5)  # Wait for 5 seconds before checking again
