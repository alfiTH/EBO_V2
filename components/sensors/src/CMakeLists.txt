cmake_minimum_required(VERSION 2.6)
PROJECT(  sensors )

INCLUDE( /home/robocomp/robocomp/cmake/robocomp.cmake )

ROBOCOMP_IDSL_TO_ICE( CommonBehavior BatteryStatus EmergencyStop EmergencyStopPub GenericBase Laser RGBSensor )
