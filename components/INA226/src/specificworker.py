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

import json
from ina226 import INA226

console = Console(highlight=False)

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
                self.paramsBattery = [float(params["maxBattery"]), float(params["minBattery"])]
            except Exception:
                print("Error reading config params")
            assert min(self.paramsBattery)>0, "Battery limits must be upper zero"
            assert self.paramsBattery[0]>self.paramsBattery[1], "Max battery must upper that min battery"
            

            with open(pathFile) as json_file:
                dataParams = json.load(json_file)
                assert check_config_json(dataParams), "Configuration has issues."
            self.powerSensor = INA226(busnum=1, address=int(dataParams["Power_sensor"],16), max_expected_amps=20, shunt_ohms=0.002)
            self.powerSensor.configure()

            self.timer.start(self.Period)
        return True


    @QtCore.Slot()
    def compute(self):
        print(self.BatteryStatus_getBatteryState())
        return True

    def startup_check(self):
        print(f"Testing RoboCompBatteryStatus.TBattery from ifaces.RoboCompBatteryStatus")
        test = ifaces.RoboCompBatteryStatus.TBattery()
        QTimer.singleShot(200, QApplication.instance().quit)

    def calc_percentage(self, voltage):
        return (((voltage - self.paramsBattery[1])*100))/ (self.paramsBattery[0]-self.paramsBattery[1])

    # =============== Methods for Component Implements ==================
    # ===================================================================

    #
    # IMPLEMENTATION of getBatteryState method from BatteryStatus interface
    #
    def BatteryStatus_getBatteryState(self):
        ret = ifaces.RoboCompBatteryStatus.TBattery()
        ret.voltage = self.powerSensor.voltage()
        ret.current = self.powerSensor.current()/1000
        ret.power = self.powerSensor.power()/1000
        ret.percentage = self.calc_percentage(voltage=ret.voltage)

        return ret
    # ===================================================================
    # ===================================================================


    ######################
    # From the RoboCompBatteryStatus you can use this types:
    # RoboCompBatteryStatus.TBattery


