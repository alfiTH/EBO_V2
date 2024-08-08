# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the TCS34725 color sensor.
# Will detect the color from the sensor and print it out every second.
import board
import adafruit_tcs34725

from vl6180x_multi import MultiSensor
from time import sleep, time

from RPi import GPIO

VL6180X_CHANNELS = [4, 17, 27,22, 10, 9, 11, 5, 6]
TCS34725 = 20
TCS34725_LED = 21
TCS34725_CHANNELS = [TCS34725, TCS34725_LED]

GPIO.setup(TCS34725_CHANNELS, GPIO.OUT)
GPIO.output(TCS34725_CHANNELS, GPIO.LOW)

ms = MultiSensor(ce_gpios=VL6180X_CHANNELS, 
                 new_i2c_addresses=[0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38], 
                 offsets=[100, 100, 100, 100, 100, 100, 100, 100, 100])

GPIO.output(TCS34725_CHANNELS, GPIO.HIGH)
sleep(0.5)

led = GPIO.PWM(TCS34725_LED, 200)
led.start(75)
# sleep(5)
# GPIO.output(5, GPIO.HIGH)


i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_tcs34725.TCS34725(i2c)



# Create sensor object, communicating over the board's default I2C bus



# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller


# Change sensor integration time to values between 2.4 and 614.4 milliseconds
# sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
sensor.gain = 4

# Main loop reading color and printing it every second.
while True:
    # Raw data from the sensor in a 4-tuple of red, green, blue, clear light component values
    print(sensor.color_raw)
    t1 = time()
    color = sensor.color
    color_rgb = sensor.color_rgb_bytes

    # Read the color temperature and lux of the sensor too.
    temp = sensor.color_temperature
    lux = sensor.lux
    print(f"\rRGB: {color_rgb} | Temperature: {temp:.2f}K | Lux: {lux:.2f} | Duration: {time()-t1:.3f} | ", end="")
    t1 = time()
    for i in range(len(VL6180X_CHANNELS)):
        print(f"Sensor {i}: {ms.get_range(i)} | ", end="")
    print(f"Duration: {time()-t1:.3f}" , end="        ")
    # Delay for a second and repeat.
    sleep(0.04)

