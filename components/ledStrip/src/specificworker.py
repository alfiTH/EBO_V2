#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Copyright (C) 2024 by YOUR NAME HERE
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

console = Console(highlight=False)

import board
import neopixel
from time import sleep
import json

sys.path.append('../../include')
from check_config_json import check_config_json



class SpecificWorker(GenericWorker):
    def __init__(self, proxy_map, startup_check=False):
        super(SpecificWorker, self).__init__(proxy_map)
        self.Period = 2000
        if startup_check:
            self.startup_check()
            self.timer = None
        else:
            self.timer.timeout.connect(self.compute)

    def __del__(self):
        """Destructor"""

    def setParams(self, params):
        if self.timer is not None:
            print("Loading config")
            try:
                pathFile = str(params["jsonConfig"])
            except Exception:
                print("Error reading config params")

            with open(pathFile) as json_file:
                dataParams = json.load(json_file)
                assert check_config_json(dataParams), "Configuration has issues."

            
            # self.ledStrip = neopixel.NeoPixel(dataParams["LED"]["GPIO"], dataParams["LED"]["Number"],  brightness=0.2, auto_write=True)
            self.timer.start(self.Period)
            
        return True


    @QtCore.Slot()
    def compute(self):
        print('SpecificWorker.compute...')


        return True

    def startup_check(self):
        print(f"Testing RoboCompLEDArray.Pixel from ifaces.RoboCompLEDArray")
        test = ifaces.RoboCompLEDArray.Pixel()
        QTimer.singleShot(200, QApplication.instance().quit)



    # =============== Methods for Component Implements ==================
    # ===================================================================

    #
    # IMPLEMENTATION of getLEDArray method from LEDArray interface
    #
    def LEDArray_getLEDArray(self):
        ret = RoboCompLEDArray.PixelArray()
        #
        # write your CODE here
        #
        return ret
    #
    # IMPLEMENTATION of setLEDArray method from LEDArray interface
    #
    def LEDArray_setLEDArray(self, pixelArray):
        ret = byte(0)
        for id, rgb in pixelArray:
            if 0 <= id < len(self.ledStrip):
                self.ledStrip[id] = (rgb.red, rgb.green, rgb.blue, rgb.white)
            else:
                ret -= -1
        #
        # write your CODE here
        #
        return ret
    # ===================================================================
    # ===================================================================


    ######################
    # From the RoboCompLEDArray you can use this types:
    # RoboCompLEDArray.Pixel


