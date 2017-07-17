#!/usr/bin/env python

from boat_cmds.py import boat_functions
from Vision.py import Vision 

MIN_ANGLE = -40 
MAX_ANGLE = 40 
MIN_THROTTLE = -120 
MAX_THROTTLE = 120
CAM_PORT = 0 
FOCAL_LENGTH = 35 
OBJ_WIDTH = 40 #mm 
CONVEYOR_ON = 20# distance from object to turn on conveyor 
CONVEYOR_LOWER = 10 #at what distance from the object should the conveyor be lowered 
COMMENT = 0 # if set to one print commands

boat = boatFunctions(MIN_ANGLE,MAX_ANGLE,MIN_THROTTLE,MAX_THROTTLE)
vision = Vision(CAM_PORT,FOCAL_LENGTH,OBJ_WIDTH)

initial_flag = 1
while not rospy.is_shutdown():
	#turn everything of to begin with 
	if initial_flag==1:
		boat.set_throttle(0) 
		boat.set_angle(0) 
		initial_flag = 0
	else:	
		#the absolute value of the angle must be more than this in order for the rudder to be set to anything other than 0
		SIGNIFICANT_RUDDER_ANGLE = 0.1
		
		#proportion of the max propeller speed that the propeller should run at based on what the conveyor belt should be doing
		SPEEDS = {"on":.25, "lowered":.5, "unlowered":1}
		
		# find left to right posistion and distance to object 
		left_val, distance = vision.find_object_position()
		
		if left_val is None: 
			print("can't find ball")
			# enter search code here 
		else:
		    angle = left_val * max_angle 

		    #stop it from correcting super slight angles
		    if abs(angle) < SIGNIFICANT_RUDDER_ANGLE:
			angle = 0

		    #move the rudder
		    boat.set_angle(angle, COMMENT)
			
		    if CONVERYOR_LOWER < distance:
			boat.set_throttle(MAX_THROTTLE*SPEEDS["unlowered"], COMMENT)

		    elif self.conveyor_on < distance and distance < self.conveyor_lower:
			boat.set_throttle(MAX_THROTTLE*SPEEDS["lowered"], COMMENT)
			boat.conveyor(False, True,COMMENT)

		    elif distance < self.conveyor_on:
			boat.set_throttle(MAX_THROTTLE*SPEEDS["on"],COMMENT)
			boat.conveyor(True,True,COMMENT)

		    else: #turn coneyor off 
			boat.set_throttle(0)
			boat.conveoyr(False,False,COMMENT)

      
     
	
