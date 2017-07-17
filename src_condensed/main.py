from boat_cmds.py import boat_functions
from Vision.py import Vision 

MIN_ANGLE = -40 
MAX_ANGLE = 40 
MIN_THROTTLE = -120 
MAX_THROTTLE = 120
CAM_PORT = 0 
FOCAL_LENGTH = 35 
OBJ_WIDTH = 40 #mm 

boat = boatFunctions(MIN_ANGLE,MAX_ANGLE,MIN_THROTTLE,MAX_THROTTLE)
vision = Vision(CAM_PORT,FOCAL_LENGTH,OBJ_WIDTH)

initial_flag = 1
while not rospy.is_shutdown():
	if initial_flag==1:
		set_speed(0)
		initial_flag = 0
	else:	
		is_left, distance = vision.find_object_posistion()
    if is_left is None: 
      print("can't find ball") 
    else: 
      
      
     
	rate.sleep()# the Rate instance keeps the loop at 10hz (which was set  above using "r = rospy.Rate(10)")
