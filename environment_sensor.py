import datetime
import random
# import Adafruit_DHT  # Uncomment if using a DHT sensor on a Raspberry Pi

class EnvironmentSensor:
    """
    A class to read environment data (temperature, humidity, and date).
    Designed to be imported and reused by other robot scripts.
    """
    
    def __init__(self, sensor_pin=None):
        """
        Initialize the sensor.
        :param sensor_pin: The GPIO pin number if using a physical sensor.
        """
        self.sensor_pin = sensor_pin
        # Example for DHT22:
        # self.sensor = Adafruit_DHT.DHT22

    def get_date(self):
        """
        Returns the current date and time as a formatted string.
        """
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def get_temperature(self):
        """
        Reads and returns the current temperature.
        """
        # --- REPLACE THIS BLOCK WITH ACTUAL SENSOR CODE ---
        # Example for Adafruit DHT:
        # humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.sensor_pin)
        # return temperature
        
        # Mocking a temperature value between 20.0 and 25.0 Celsius
        mock_temp = random.uniform(20.0, 25.0)
        return round(mock_temp, 2)

    def get_humidity(self):
        """
        Reads and returns the current humidity.
        """
        # --- REPLACE THIS BLOCK WITH ACTUAL SENSOR CODE ---
        # Example for Adafruit DHT:
        # humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.sensor_pin)
        # return humidity
        
        # Mocking a humidity value between 40.0% and 60.0%
        mock_humidity = random.uniform(40.0, 60.0)
        return round(mock_humidity, 2)

    def get_all_data(self):
        """
        Convenience method to retrieve all data points at once.
        Returns a dictionary containing date, temperature, and humidity.
        """
        return {
            "date": self.get_date(),
            "temperature": self.get_temperature(),
            "humidity": self.get_humidity()
        }


# ==========================================
# Example usage / Testing the script directly
# ==========================================
if __name__ == "__main__":
    # Initialize the class
    sensor = EnvironmentSensor(sensor_pin=4)
    
    # Call individual methods
    current_date = sensor.get_date()
    current_temp = sensor.get_temperature()
    current_hum = sensor.get_humidity()
    
    print(f"Date: {current_date}")
    print(f"Temperature: {current_temp} °C")
    print(f"Humidity: {current_hum} %")
    print("-" * 20)
    
    # Call the batched method
    all_data = sensor.get_all_data()
    print("All Data Dictionary:", all_data)
