import sys
import os
import random

# Añade el directorio lib al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'venv/lib/python3.12/site-packages')))

import board
import neopixel
from time import sleep

NUMLEDS : int = 54

pixels = neopixel.NeoPixel(getattr(board, "D"+"18"), NUMLEDS,  brightness=0.5, auto_write=True)
pixels.fill((0,0,0))
sleep(5)

pixels.fill((255, 0, 0))
sleep(1)
pixels.fill((0, 255, 255))
sleep(1)
pixels.fill((255, 255, 255))
sleep(1)

pixels[0] = (255, 255, 0)

for x in range(NUMLEDS):
    pixels[x] = (255, 0, 255)
    sleep(.1)

pixels.fill((0, 0, 0))

for x in range(NUMLEDS):
    pixels[x] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    sleep(0.1)

sleep(1)

pixels.fill((0, 0, 0))
