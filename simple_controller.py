#!/usr/bin/env python

import rospy
import sys
import time
import random


from gps_common.msg import GPSFix
from gps_common.msg import GPSStatus
from sensor_msgs.msg import NavSatFix

from std_msgs.msg import Float32
from std_msgs.msg import Int8


total_time = 0
cnt = 0


# Publishing topic names
RUDDER_PUB_TOPIC = "motor_cmd/steer"
PROP_PUB_TOPIC = "motor_cmd/propeller"

# Subscribing topic names
RUDDER_SUB_TOPIC = "sensors/steer"
PROP_SUB_TOPIC = "sensors/propeller"
COMPASS_SUB_TOPIC = "sensors/compass"
CURRENT_SUB_TOPIC = "sensors/current"
VOLTAGE_SUB_TOPIC = "sensors/voltage"
OVERRIDE_SUB_TOPIC = "sensors/remote_is_overriding"

GPS_FIX_SUB_TOPIC = "fix"
#GPS_EXT_FIX_SUB_TOPIC = "extended_fix"



def callback_gps_fix(msg):
	print("latitude :", msg.latitude)
	print("longitude :", msg.longitude)
	print("error covariance :", msg.position_covariance)
	
def callback_compass(msg):
	print("heading: ", msg.data)


def set_speed(vel):
	global pub_prop
	print("set_speed : ", vel)
	pub_prop.publish(vel)

def set_steer(ang):
	global pub_rudder
	# ang must be between -30 deg and +30 deg
	print("set_steer : ", ang)
	pub_rudder.publish(ang)

def controller():
	global cnt
	global total_time

	MISSION_DURATION = 60
	BOAT_SPEED = 30
	HEADING_CHANGE_TIME = 10


	# set a fixed speed at the beginning
	# After 60 seconds, stop the boat
	if total_time==0:
		set_speed(BOAT_SPEED)
	elif total_time == MISSION_DURATION:
		set_speed(0)

	# changes the heading between -20 and 20 degrees every HEADING_CHANGE_TIME seconds						
	if cnt==HEADING_CHANGE_TIME and total_time>0 and total_time<MISSION_DURATION:
		angle = random.randint(-20,21)
		set_steer(angle)
		cnt = 0

	cnt = cnt + 1
	total_time = total_time + 1	


########### Main ########### 


# start the ros node
rospy.init_node('simple_controller', anonymous=True)
rate = rospy.Rate(1) # 10hz


# Publishers
pub_prop = rospy.Publisher(PROP_PUB_TOPIC, Int8, queue_size=1)
pub_rudder = rospy.Publisher(RUDDER_PUB_TOPIC, Int8, queue_size=1)


# Subscribers
rospy.Subscriber(GPS_FIX_SUB_TOPIC, NavSatFix, callback_gps_fix)
#rospy.Subscriber(GPS_EXT_FIX_SUB_TOPIC, GPSFix, callback_ext_gps_fix)

rospy.Subscriber(COMPASS_SUB_TOPIC, Float32, callback_compass)

initial_flag = 1
while not rospy.is_shutdown():
	if initial_flag==1:
		set_speed(0)
		initial_flag = 0
	else:	
		controller()
	rate.sleep()# the Rate instance keeps the loop at 10hz (which was set  above using "r = rospy.Rate(10)")
