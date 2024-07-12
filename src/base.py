import sys
import os

# Añade el directorio lib al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'include')))

# Ahora puedes importar L298N
from L298N import L298N

from time import sleep

base = L298N(13, 23, 24, 17, 27, 12)
base.setStateMotor(True)
base.setSpeed(50,0)
sleep(4)
base.setSpeed(0,50)
sleep(4)

base.setSpeed(50,50)
sleep(4)

base.setSpeed(-100,-100)
sleep(4)