import argparse
import json
from collections import Counter

def check_config_json(data):
    # Extract GPIO pins
    gpio_pins = []

    # Extract GPIO pins from LiDARs
    lidars = data.get("LiDARs")
    if lidars is None:
        print("LiDARs key is missing.")
        return False
    for lidar in lidars:
        gpio_pins.append(lidar["GPIO"])

    # Extract GPIO pins from RGB_sensor
    rgb_sensor = data.get("RGB_sensor")
    if rgb_sensor is None:
        print("RGB_sensor key is missing.")
        return False
    gpio_pins.append(rgb_sensor["GPIO_sensor"])
    gpio_pins.append(rgb_sensor["GPIO_led"])

    # Extract GPIO pins from Drives
    drives = data.get("Drives")
    if drives is None:
        print("Drives key is missing.")
        return False
    for pin in ["ENA", "IN1", "IN2", "ENB", "IN3", "IN4"]:
        if pin in drives:
            gpio_pins.append(drives[pin])
        else:
            print(f"{pin} is missing in Drives.")
            return False

    # Extract GPIO pin for LED
    led = data.get("LED")
    if led is None or led["GPIO"] is None:
        print("LED key is missing.")
        return False
    gpio_pins.append(led["GPIO"])

    # Check for duplicates
    gpio_counter = Counter(gpio_pins)
    duplicates = [pin for pin, count in gpio_counter.items() if count > 1]

    if len(duplicates) > 0:
        print("GPIO pins repeated:", duplicates)
        return False
    else:
        print("No GPIO pins are repeated.")
        return True

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                    prog='check_config_json',
                    description='Checking format config JSON')
    
    parser.add_argument('filename', type=str)     
    args = parser.parse_args()
    
    # Load JSON data
    with open(args.filename) as json_file:
        data = json.load(json_file)

    if check_config_json(data):
        print("Configuration is valid.")
    else:
        print("Configuration has issues.")

