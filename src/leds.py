import sys
import os
import random

# Añade el directorio lib al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'venv/lib/python3.12/site-packages')))

import board
import neopixel
from time import sleep

pixels = neopixel.NeoPixel(board.D18, 14,  brightness=0.2, auto_write=True)
pixels.fill((255, 0, 0))
sleep(1)

pixels[0] = (255, 255, 0)

for x in range(0, 14):
    pixels[x] = (255, 0, 255)
    sleep(.5)

pixels.fill((0, 0, 0))

for x in range(0, 14):
    pixels[x] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    sleep(0.1)

sleep(1)

pixels.fill((0, 0, 0))
