#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Code by Daniel Ellis, Fiona Shyne and London Lowmanstone

import rospy
import sys
import time

from gps_common.msg import GPSFix
from gps_common.msg import GPSStatus

from sensor_msgs.msg import NavSatFix

from std_msgs.msg import Float32
from std_msgs.msg import Int8

class boatFunctions:
    
    def __init__(self, min_angle, max_angle, min_throttle, max_throttle):

        rospy.init_node('boat_cmds', anonymous=True)
        self.rate = rospy.Rate(1) # 10hz

        #Rudder
        self.RUDDER_PUB_TOPIC = "motor_cmd/steer"
        self.pub_rudder = rospy.Publisher(self.RUDDER_PUB_TOPIC, Int8, queue_size=1)
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.angle = min_angle
        
        #Propeller
        self.PROP_PUB_TOPIC = "motor_cmd/propeller"
        self.pub_prop = rospy.Publisher(self.PROP_PUB_TOPIC, Int8, queue_size=1)
        self.max_throttle = max_throttle
        self.min_throttle = min_throttle
        self.throttle_on = False
        self.throttle = 0
	
        
        #Conveyor
        self.conveyor_on = False
        self.conveyor_lowered = False
        
        #GPS
        self.GPS_FIX_SUB_TOPIC = "fix"
        self.gps = rospy.Subscriber(self.GPS_FIX_SUB_TOPIC, NavSatFix, self.gps_msg)
        
        #Compass
        self.COMPASS_SUB_TOPIC = "sensors/compass"
        self.compass = rospy.Subscriber(self.COMPASS_SUB_TOPIC, Float32, self.compass_msg)
        
	self.rate.sleep()

    def set_angle(self, angle, comment=0):
        if angle <= self.min_angle:
            angle = self.min_angle
        if angle >= self.max_angle:
            angle = self.max_angle
        if comment == 1:
            print("{}: Setting angle to {}" .format(time.time(), angle))
        self.pub_rudder.publish(angle)
        self.angle = angle
        self.rate.sleep()
        
    def set_throttle(self, throttle, comment=0):
        if throttle == 0:
            self.throttle_on == False
        else:
            self.throttle_on == True
        if throttle <= self.min_throttle:
            throttle = self.min_throttle
        if throttle >= self.max_throttle:
            throttle = self.max_throttle
        if comment == 1:
            print("{}: Setting throttle to {}" .format(time.time(), throttle))
        self.pub_prop.publish(throttle)
        self.throttle = throttle
        self.rate.sleep()
        
    def conveyor(self, on, lowered, comment=0):
        if isinstance(on, bool): 
            self.coneveyor_on = on
        else: 
            print("Error: cannot understand on variable please enter a bool")
            
        if isinstance(lowered, bool): 
            self.coneveyor_lowered = lowered
        else: 
            print("Error: icannot understand lowered variable please enter a bool")
            
        if comment == 1: 
            print("{}: The Conveyor is {} and {}" .format(time.time(), on, lowered))
        self.rate.sleep()

    def gps_msg(self, msg):
        print("latitude :", msg.latitude)
        print("longitude :", msg.longitude)
        print("error covariance :", msg.position_covariance)
        self.rate.sleep()
        
    def compass_msg(self, msg):
        print("heading: ", msg.data)
        self.rate.sleep()

boat = boatFunctions(-40,40,-120,120)
boat.set_angle(0,1)
boat.set_throttle(0, 1)
