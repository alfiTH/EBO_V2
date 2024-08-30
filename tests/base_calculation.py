import sys
import os

# Añade el directorio lib al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'include')))

# Ahora puedes importar L298N
from L298N import L298N

from time import sleep

base = L298N(13, 19, 26, 16, 20, 12)
base.setStateMotor(True)

#Tres vueltas
base.setSpeed(-100, 100)
sleep(3.6923)

#Dos metros
#base.setSpeed(100, 100)
#sleep(26.49)