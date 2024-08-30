# EBO_V2
en este repo se encotrará el software necesario para el motaje de la nueva version del EBO, robot diseñado y constuido por la universidad de Extremadura, Robolab.


# Prerequisitos

## Crear entorno vitual si lo desea
```bash
python3 -m venv venv
source venv/bin/activate
```

## Librerias

```bash
cd ~/software || mkdir ~/software && cd ~/software
git clone https://github.com/alfiTH/vl6180x_multi
cd vl6180x_multi
pip3 install .

pip3 install rpi_ws281x adafruit-circuitpython-tcs34725 adafruit-circuitpython-neopixel
```

## Permisos GPIO
### Mediante chmod
```bash
sudo chmod 666 /dev/gpio*
```

### Mediante reglas udeb
```bash
sudo nano /etc/udev/rules.d/99-gpio.rules

SUBSYSTEM=="gpio*", PROGRAM="/bin/sh -c 'chown -R root:gpio /sys/class/gpio && chmod -R 770 /sys/class/gpio; chown -R root:gpio /dev/gpio* && chmod -R 770 /dev/gpio*'"

sudo udevadm control --reload-rules
sudo udevadm trigger
```

# Tests
## Sensor de color y Lidars
```bash
python src/sensors.py
```

## Tira led
```bash
sudo --preserve-env=PATH,VIRTUAL_ENV python3 leds.py
```

## Base
```bash
python src/base.py
```
