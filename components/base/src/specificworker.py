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


console = Console(highlight=False)
sys.path.append('../../include')
from check_config_json import check_config_json
from L298N import L298N

#TODO CALCULATE
ROT_CONST = 100/75.5 #max speed 75.5mm/s
ADV_CONST = 100/0.8125 #max rot speed 0.8125rad/s

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
        self.base.setStateMotor(False)

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
            self.base = L298N(dataParams["ENA"], dataParams["IN1"], dataParams["IN2"], 
                              dataParams["ENB"], dataParams["IN3"], dataParams["IN4"])
            self.base.setStateMotor(True)

            self.timer.start(self.Period)
        return True



    @QtCore.Slot()
    def compute(self):
        return True

    def startup_check(self):
        print(f"Testing RoboCompDifferentialRobot.TMechParams from ifaces.RoboCompDifferentialRobot")
        test = ifaces.RoboCompDifferentialRobot.TMechParams()
        QTimer.singleShot(200, QApplication.instance().quit)



    # =============== Methods for Component Implements ==================
    # ===================================================================

    #
    # IMPLEMENTATION of correctOdometer method from DifferentialRobot interface
    #
    def DifferentialRobot_correctOdometer(self, x, z, alpha):
        pass


    #
    # IMPLEMENTATION of getBasePose method from DifferentialRobot interface
    #
    def DifferentialRobot_getBasePose(self):
        return [x, z, alpha]
    #
    # IMPLEMENTATION of getBaseState method from DifferentialRobot interface
    #
    def DifferentialRobot_getBaseState(self):
        state = RoboCompGenericBase.TBaseState()
        return state
    #
    # IMPLEMENTATION of resetOdometer method from DifferentialRobot interface
    #
    def DifferentialRobot_resetOdometer(self):
        pass


    #
    # IMPLEMENTATION of setOdometer method from DifferentialRobot interface
    #
    def DifferentialRobot_setOdometer(self, state):
        pass


    #
    # IMPLEMENTATION of setOdometerPose method from DifferentialRobot interface
    #
    def DifferentialRobot_setOdometerPose(self, x, z, alpha):
        pass


    #
    # IMPLEMENTATION of setSpeedBase method from DifferentialRobot interface
    #
    def DifferentialRobot_setSpeedBase(self, adv, rot):
        advSpeed = adv * ADV_CONST
        rotSpeed = rot * ROT_CONST

        self.base.setSpeed(max(min(advSpeed + rotSpeed, 100), -100), 
                           max(min(advSpeed - rotSpeed, 100), -100))



    #
    # IMPLEMENTATION of stopBase method from DifferentialRobot interface
    #
    def DifferentialRobot_stopBase(self):
        self.base.setSpeed(0, 0)


    # ===================================================================
    # ===================================================================


    ######################
    # From the RoboCompDifferentialRobot you can use this types:
    # RoboCompDifferentialRobot.TMechParams


