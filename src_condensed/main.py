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
