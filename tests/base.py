import sys
import os

# Añade el directorio lib al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'include')))

# Ahora puedes importar L298N
from L298N import L298N

from time import sleep
PERIOD = 1.5

base = L298N(13, 19, 26, 16, 20, 12)
base.setStateMotor(True)

sleep(PERIOD)

base.setSpeed(30,30)
sleep(PERIOD)

base.setSpeed(-50,-50)
sleep(PERIOD)

base.setSpeed(75,75)
sleep(PERIOD)

base.setSpeed(-100,-100)
sleep(PERIOD)

base.setSpeed(30,-30)
sleep(PERIOD)

base.setSpeed(50,-50)
sleep(PERIOD)

base.setSpeed(-75,75)
sleep(PERIOD)

base.setSpeed(100,-100)
sleep(PERIOD)
