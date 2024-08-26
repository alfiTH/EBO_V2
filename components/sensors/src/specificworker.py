#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Copyright (C) 2024 by Alejandro Torrejón Harto
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from rich.console import Console
from genericworker import *
import interfaces as ifaces

import board
import adafruit_tcs34725

from vl6180x_multi import MultiSensor
from time import sleep, time

from RPi import GPIO

import json

sys.path.append('../../include')
from check_config_json import check_config_json

console = Console(highlight=False)


class SpecificWorker(GenericWorker):
    def __init__(self, proxy_map, startup_check=False):
        super(SpecificWorker, self).__init__(proxy_map)
        self.Period = 50

        self.emergency = False

        if startup_check:
            self.startup_check()
            self.timer=None
        else:
            self.timer.timeout.connect(self.compute)
            

    def __del__(self):
        """Destructor"""
        GPIO.output([item["GPIO"] for item in self.params["LiDARs"]] + 
                     list(self.params["RGB_sensor"].values()), GPIO.LOW)

    def setParams(self, params):
        if self.timer is not None:
            print("Loading config")
            try:
                pathFile = str(params["jsonConfig"])
            except Exception:
                print("Error reading config params")

            with open(pathFile) as json_file:
                self.params = json.load(json_file)
                assert check_config_json(self.params), "Configuration has issues."

            print("Configuring GPIOs")
            GPIO.setup(list(self.params["RGB_sensor"].values()), GPIO.OUT, initial=GPIO.LOW)

            mode_gpio = self.params.get("mode_gpio")
            if mode_gpio is None:
                mode_gpio = GPIO.BCM
            else:
                mode_gpio = getattr(GPIO, mode_gpio)
                
            self.LiDARs = MultiSensor([item["id"] for item in self.params["LiDARs"]], 
                            gpios=[item["GPIO"] for item in self.params["LiDARs"]], 
                            new_i2c_addresses=[int(item["new_i2c_address"], 16) for item in self.params["LiDARs"]], 
                            offsets=[item["offset"] for item in self.params["LiDARs"]], mode_gpio=mode_gpio)

            GPIO.output(self.params["RGB_sensor"]["GPIO_sensor"], GPIO.HIGH)
            self.ledSensor = GPIO.PWM(self.params["RGB_sensor"]["GPIO_led"], 200)
            self.ledSensor.start(0)
            sleep(0.5)

            i2c = board.I2C()  # uses board.SCL and board.SDA
            self.RGBSensor = adafruit_tcs34725.TCS34725(i2c)
            self.RGBSensor.gain = 4 # Change sensor gain to 1, 4, 16, or 60
        
            self.LiDARsValue = ifaces.RoboCompLaser.TLaserData()

            print("Start compute")
            self.timer.start(self.Period)
        return True


    @QtCore.Slot()
    def compute(self):
        distance_fall = self.LiDARs.get_range("anti-fall")
        if self.emergency:
            if distance_fall==0:
                self.emergency = False
                self.emergencystoppub_proxy.emergencyStop(self.emergency)
                
        else:
            if distance_fall!=0:
                self.emergency = True 
                self.emergencystoppub_proxy.emergencyStop(self.emergency)

        auxLiDARsValue = ifaces.RoboCompLaser.TLaserData()
        for item in self.params["LiDARs"]:
            if "angle" in item:
                auxLiDARsValue.append(ifaces.RoboCompLaser.TData(angle=item["angle"], dist=self.LiDARs.get_range(item["id"])))
        self.LiDARsValue = auxLiDARsValue

        print(self.LiDARs.get_range("anti-fall"))
        print(self.EmergencyStop_isEmergency())
        print(self.Laser_getLaserData())
        print(self.RGBSensor_getRGBPixel())

    def startup_check(self):
        print(f"Testing RoboCompLaser.LaserConfData from ifaces.RoboCompLaser")
        test = ifaces.RoboCompLaser.LaserConfData()
        print(f"Testing RoboCompLaser.TData from ifaces.RoboCompLaser")
        test = ifaces.RoboCompLaser.TData()
        print(f"Testing RoboCompRGBSensor.RGBPixel from ifaces.RoboCompRGBSensor")
        test = ifaces.RoboCompRGBSensor.RGBPixel()
        print(f"Testing RoboCompRGBSensor.RGBPixelRAW from ifaces.RoboCompRGBSensor")
        test = ifaces.RoboCompRGBSensor.RGBPixelRAW()
        QTimer.singleShot(200, QApplication.instance().quit)


    # =============== Methods for Component Implements ==================
    # ===================================================================

    #
    # IMPLEMENTATION of isEmergency method from EmergencyStop interface
    #
    def EmergencyStop_isEmergency(self):
        return self.emergency
    #
    # IMPLEMENTATION of getLaserAndBStateData method from Laser interface
    #
    def Laser_getLaserAndBStateData(self):
        ret = ifaces.RoboCompLaser.TLaserData()
        return [ret, bState]
    #
    # IMPLEMENTATION of getLaserConfData method from Laser interface
    #
    def Laser_getLaserConfData(self):
        ret = ifaces.RoboCompLaser.LaserConfData()
        return ret
    #
    # IMPLEMENTATION of getLaserData method from Laser interface
    #
    def Laser_getLaserData(self):
        return self.LiDARsValue
    #
    # IMPLEMENTATION of getLux method from RGBSensor interface
    #
    def RGBSensor_getLux(self):
        return self.RGBSensor.lux
    #
    # IMPLEMENTATION of getRGBPixel method from RGBSensor interface
    #
    def RGBSensor_getRGBPixel(self):
        colorRGB = self.RGBSensor.color_rgb_bytes
        return ifaces.RoboCompRGBSensor.RGBPixel(red=colorRGB[0], green=colorRGB[1], blue=colorRGB[2])
    #
    # IMPLEMENTATION of getRGBPixelRAW method from RGBSensor interface
    #
    def RGBSensor_getRGBPixelRAW(self):
        colorRAW = self.RGBSensor.color_raw
        return ifaces.RoboCompRGBSensor.RGBPixelRAW(red=colorRAW[0], green=colorRAW[1], blue=colorRAW[2], clearLight=colorRAW[3])
    #
    # IMPLEMENTATION of getTemperature method from RGBSensor interface
    #
    def RGBSensor_getTemperature(self):
        return self.RGBSensor.color_temperature
    #
    # IMPLEMENTATION of setLight method from RGBSensor interface
    #
    def RGBSensor_setLight(self, percentageLight):
        self.ledSensor.ChangeDutyCycle(min(max(percentageLight, 0), 100))
    # ===================================================================
    # ===================================================================


    ######################
    # From the RoboCompEmergencyStopPub you can publish calling this methods:
    # self.emergencystoppub_proxy.emergencyStop(...)

    ######################
    # From the RoboCompLaser you can use this types:
    # RoboCompLaser.LaserConfData
    # RoboCompLaser.TData

    ######################
    # From the RoboCompRGBSensor you can use this types:
    # RoboCompRGBSensor.RGBPixel
    # RoboCompRGBSensor.RGBPixelRAW


