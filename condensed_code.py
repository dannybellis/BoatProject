#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import sys
import time
import math

from gps_common.msg import GPSFix
from gps_common.msg import GPSStatus

from sensor_msgs.msg import NavSatFix

from std_msgs.msg import Float32
from std_msgs.msg import Int8
from std_msgs.msg import Bool


import cv2
from cv_bridge import *



MIN_ANGLE = -40 
MAX_ANGLE = 40 
MIN_THROTTLE = -120 
MAX_THROTTLE = 120
CAM_PORT = 0 
FOCAL_LENGTH = 45 
OBJ_WIDTH = 40 #mm 
CONVEYOR_ON = 20# distance from object to turn on conveyor 
CONVEYOR_LOWER = 10 #at what distance from the object should the conveyor be lowered 
COMMENT = 1 # if set to one print commands
SIGNIFICANT_RUDDER_ANGLE = 0.1 # change in angle must be more then this 
EXTRA_COMMENT = 0 #if set to one print extra comments like longitude 

class boatFunctions:
    
    def __init__(self, min_angle, max_angle, min_throttle, max_throttle, extra_comment = 0):

        rospy.init_node('boat_cmds', anonymous=True)
        self.rate = rospy.Rate(1) # 10hz
	
	self.extra_comment = extra_comment 

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
		self.LOWER_PUB_TOPIC = "motor_cmd/conveyor_lower" 
		self.CONVEYOR_ON_PUB_TOPIC = "motor_cmd/conveyor_on"
		self.pub_conveyor_lower = rospy.Publisher(self.LOWER_PUB_TOPIC,Bool,queue_size = 1) 
		self.pub_conveyor_on = rospy.Publisher(self.CONVEYOR_ON_PUB_TOPIC,Bool,queue_size = 1)
        self.conveyor_on = False
        self.conveyor_lowered = False
        
        #GPS
        self.GPS_FIX_SUB_TOPIC = "fix"
        self.gps = rospy.Subscriber(self.GPS_FIX_SUB_TOPIC, NavSatFix, self.gps_msg)
	self.lat = 0
	self.lon = 0
        
        #Compass
        self.COMPASS_SUB_TOPIC = "sensors/compass"
        self.compass = rospy.Subscriber(self.COMPASS_SUB_TOPIC, Float32, self.compass_msg)
	self.heading = 0
	
	#Targeting
	self.target_lat = target_lat
	self.target_lon = target_lon
	self.target_angle = 0
	
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
			self.pub_conveyor_on.publish(on)
        else: 
            print("Error: cannot understand on variable please enter a bool")
            
        if isinstance(lowered, bool): 
            self.coneveyor_lowered = lowered
			self.pub_conveyor_lowered.publish(on)
        else: 
            print("Error: cannot understand lowered variable please enter a bool")
            
        if comment == 1: 
            print("{}: The Conveyor is {} and {}" .format(time.time(), on, lowered))
        self.rate.sleep()

    def gps_msg(self, msg):
	if self.extra_comment == 1:
           print("latitude :", msg.latitude)
           print("longitude :", msg.longitude)
           print("error covariance :", msg.position_covariance)
	   self.lat = msg.latitude
	   self.lon = msg.longitude
           self.rate.sleep()
        
    def compass_msg(self, msg):
	if self.extra_comment == 1:
           print("heading: ", msg.data)
	   self.heading = msg.data
           self.rate.sleep()
	
    def target_heading_direction(self)
	self.compass_msg()
	self.gps_msg()
	lat1 = radians(self.lat)
	lon1 = radians(self.lon)
	lat2 = radians(self.target_lat)
	lon2 = radians(self.target_lon)
	target_heading = math.atan2(math.sin(lon2-lon1)*math.cos(lat2), (math.cos(lat1)*math.sin(lat2))-(math.sin(lat1)*math.cos(lat2)*math.cos(lon2-lon1)))
	self.target_angle = math.degrees(target_heading)
	self.rate.sleep()	




def search(): 
   print("searching for ball") 
   if not boat.throttle == MAX_THROTTLE* 0.6:
      boat.set_throttle(MAX_THROTTLE / 0.6) 

   if not boat.angle == 10: 
      boat.set_angle(10) 

#returns a list of the contours of the ball
class Vision:
    """
    An OpenCV pipeline generated by GRIP.
    """
    
    def __init__(self, camera_port, focal_length, object_width):
        """initializes all values to presets or None if need to be set
        """
        self.cam = cv2.VideoCapture(camera_port)
        self.focal_length = focal_length
        self.object_width = object_width 
	
	
        self.__hsv_threshold_hue = [9.712230215827338, 34.095563139931755]
        self.__hsv_threshold_saturation = [2.293165467625899, 239.76962457337888]
        self.__hsv_threshold_value = [231.60971223021585, 255.0]

        self.hsv_threshold_output = None

        self.__cv_erode_src = self.hsv_threshold_output
        self.__cv_erode_kernel = None
        self.__cv_erode_anchor = (-1, -1)
        self.__cv_erode_iterations = 3.0
        self.__cv_erode_bordertype = cv2.BORDER_CONSTANT
        self.__cv_erode_bordervalue = (-1)

        self.cv_erode_output = None

        """self.__blur_input = self.cv_erode_output
	BlurType = Enum('BlurType', 'Box_Blur Gaussian_Blur Median_Filter Bilateral_Flilter')
        self.__blur_type = BlurType.Gaussian_Blur
        self.__blur_radius = 1.801801801801802

        self.blur_output = None/"""

        self.__cv_threshold_src = self.cv_erode_output
        self.__cv_threshold_thresh = 1.0
        self.__cv_threshold_maxval = 255.0
        self.__cv_threshold_type = cv2.THRESH_BINARY

        self.cv_threshold_output = None

        self.__find_contours_input = self.cv_threshold_output
        self.__find_contours_external_only = False

        self.find_contours_output = None

        self.__filter_contours_contours = self.find_contours_output
        self.__filter_contours_min_area = 2.0
        self.__filter_contours_min_perimeter = 2.0
        self.__filter_contours_min_width = 0
        self.__filter_contours_max_width = 1000
        self.__filter_contours_min_height = 0
        self.__filter_contours_max_height = 1000
        self.__filter_contours_solidity = [29.67625899280576, 100]
        self.__filter_contours_max_vertices = 1000000
        self.__filter_contours_min_vertices = 5.0
        self.__filter_contours_min_ratio = 1.0
        self.__filter_contours_max_ratio = 1000

        self.filter_contours_output = None


    def process(self, source0):
         # Step HSV_Threshold0:
        self.__hsv_threshold_input = source0
        (self.hsv_threshold_output) = self.__hsv_threshold(self.__hsv_threshold_input, self.__hsv_threshold_hue, self.__hsv_threshold_saturation, self.__hsv_threshold_value)

        # Step CV_erode0:
        self.__cv_erode_src = self.hsv_threshold_output
        (self.cv_erode_output) = self.__cv_erode(self.__cv_erode_src, self.__cv_erode_kernel, self.__cv_erode_anchor, self.__cv_erode_iterations, self.__cv_erode_bordertype, self.__cv_erode_bordervalue)

        # Step Blur0:
        #self.__blur_input = self.cv_erode_output
        #(self.blur_output) = self.__blur(self.__blur_input, self.__blur_type, self.__blur_radius)

        # Step CV_Threshold0:
        self.__cv_threshold_src = self.cv_erode_output
        (self.cv_threshold_output) = self.__cv_threshold(self.__cv_threshold_src, self.__cv_threshold_thresh, self.__cv_threshold_maxval, self.__cv_threshold_type)

        # Step Find_Contours0:
        self.__find_contours_input = self.cv_threshold_output
        (self.find_contours_output) = self.__find_contours(self.__find_contours_input, self.__find_contours_external_only)

        # Step Filter_Contours0:
        self.__filter_contours_contours = self.find_contours_output
        self.contours = self.__filter_contours(self.__filter_contours_contours, self.__filter_contours_min_area, self.__filter_contours_min_perimeter, self.__filter_contours_min_width, self.__filter_contours_max_width, self.__filter_contours_min_height, self.__filter_contours_max_height, self.__filter_contours_solidity, self.__filter_contours_max_vertices, self.__filter_contours_min_vertices, self.__filter_contours_min_ratio, self.__filter_contours_max_ratio)
        
        # if there are no contours return can't find ball 
        if len(self.contours) == 0:
            return ("can't find ball")

        #find the bigest contour and set it to best contour
        mas_area = 0
        best_contour= 0
        for i in self.contours:
            area = cv2.contourArea(i)
        if area > mas_area:
            mas_area = area
            best_contour= i
        return best_contour   

    @staticmethod
    def __hsv_threshold(input, hue, sat, val):
        """Segment an image based on hue, saturation, and value ranges.
        Args:
            input: A BGR numpy.ndarray.
            hue: A list of two numbers the are the min and max hue.
            sat: A list of two numbers the are the min and max saturation.
            lum: A list of two numbers the are the min and max value.
        Returns:
            A black and white numpy.ndarray.
        """
        out = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)
        return cv2.inRange(out, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))

    @staticmethod
    def __cv_erode(src, kernel, anchor, iterations, border_type, border_value):
        """Expands area of lower value in an image.
        Args:
           src: A numpy.ndarray.
           kernel: The kernel for erosion. A numpy.ndarray.
           iterations: the number of times to erode.
           border_type: Opencv enum that represents a border type.
           border_value: value to be used for a constant border.
        Returns:
            A numpy.ndarray after erosion.
        """
        return cv2.erode(src, kernel, anchor, iterations = (int) (iterations +0.5),
                            borderType = border_type, borderValue = border_value)

    @staticmethod
    def __blur(src, type, radius):
        """Softens an image using one of several filters.
        Args:
            src: The source mat (numpy.ndarray).
            type: The blurType to perform represented as an int.
            radius: The radius for the blur as a float.
        Returns:
            A numpy.ndarray that has been blurred.
        """
        if(type is BlurType.Box_Blur):
            ksize = int(2 * round(radius) + 1)
            return cv2.blur(src, (ksize, ksize))
        elif(type is BlurType.Gaussian_Blur):
            ksize = int(6 * round(radius) + 1)
            return cv2.GaussianBlur(src, (ksize, ksize), round(radius))
        elif(type is BlurType.Median_Filter):
            ksize = int(2 * round(radius) + 1)
            return cv2.medianBlur(src, ksize)
        else:
            return cv2.bilateralFilter(src, -1, round(radius), round(radius))

    @staticmethod
    def __cv_threshold(src, thresh, max_val, type):
        """Apply a fixed-level threshold to each array element in an image
        Args:
            src: A numpy.ndarray.
            thresh: Threshold value.
            max_val: Maximum value for THRES_BINARY and THRES_BINARY_INV.
            type: Opencv enum.
        Returns:
            A black and white numpy.ndarray.
        """
        return cv2.threshold(src, thresh, max_val, type)[1]

    @staticmethod
    def __find_contours(input, external_only):
        """Sets the values of pixels in a binary image to their distance to the nearest black pixel.
        Args:
            input: A numpy.ndarray.
            external_only: A boolean. If true only external contours are found.
        Return:
            A list of numpy.ndarray where each one represents a contour.
        """
        if(external_only):
            mode = cv2.RETR_EXTERNAL
        else:
            mode = cv2.RETR_LIST
        method = cv2.CHAIN_APPROX_SIMPLE
        contours, hierarchy =cv2.findContours(input, mode=mode, method=method)
        return contours

    @staticmethod
    def __filter_contours(input_contours, min_area, min_perimeter, min_width, max_width,
                        min_height, max_height, solidity, max_vertex_count, min_vertex_count,
                        min_ratio, max_ratio):
        """Filters out contours that do not meet certain criteria.
        Args:
            input_contours: Contours as a list of numpy.ndarray.
            min_area: The minimum area of a contour that will be kept.
            min_perimeter: The minimum perimeter of a contour that will be kept.
            min_width: Minimum width of a contour.
            max_width: MaxWidth maximum width.
            min_height: Minimum height.
            max_height: Maximimum height.
            solidity: The minimum and maximum solidity of a contour.
            min_vertex_count: Minimum vertex Count of the contours.
            max_vertex_count: Maximum vertex Count.
            min_ratio: Minimum ratio of width to height.
            max_ratio: Maximum ratio of width to height.
        Returns:
            Contours as a list of numpy.ndarray.
        """
        output = []
        for contour in input_contours:
            x,y,w,h = cv2.boundingRect(contour)
            if (w < min_width or w > max_width):
                continue
            if (h < min_height or h > max_height):
                continue
            area = cv2.contourArea(contour)
            if (area < min_area):
                continue
            if (cv2.arcLength(contour, True) < min_perimeter):
                continue
            hull = cv2.convexHull(contour)
            solid = 100 * area / cv2.contourArea(hull)
            if (solid < solidity[0] or solid > solidity[1]):
                continue
            if (len(contour) < min_vertex_count or len(contour) > max_vertex_count):
                continue
            ratio = (float)(w) / h
            if (ratio < min_ratio or ratio > max_ratio):
                continue
            output.append(contour)
        return output
        
    # returns a value between -1 and 1, negative means the object is to the right of the viewer, positive means left
    def is_left(self,img):
        HEIGHT, WIDTH, channel = img.shape
        contours = self.process(img)
        if contours == "can't find ball":
            return "can't find ball"
        middle = WIDTH / 2
        #find the average of the bigest x value and the smallest x value of contours
        lst = []
        for i in contours:
            lst.append(i[0][0] - middle)
        max_lst = float(max(lst))
        min_lst = float(min(lst))
        average = (max_lst + min_lst) / 2
        return -(average / middle)
    
    #returns the distance between an object and the camera        
    def find_distance(self,img):
        contours = self.process(img)
        if len(contours) == 0:
            return 0 
        (x,y), radius = cv2.minEnclosingCircle(contours)
        px_width = radius * 2
        return (self.object_width * self.focal_length) / px_width
        
    def find_object_position(self):
        ret,frame = self.cam.read()
	if frame is None: 
            return "camera", None
        is_left = self.is_left(frame)
        if is_left == "can't find ball": 
            return None, None 
        distance = self.find_distance(frame)
        return is_left, distance
			

boat = boatFunctions(MIN_ANGLE,MAX_ANGLE,MIN_THROTTLE,MAX_THROTTLE, EXTRA_COMMENT)
vision = Vision(CAM_PORT,FOCAL_LENGTH,OBJ_WIDTH)

search_count = 0 #count how many times it can't find the ball 
find_count = 0 #count how many times it can find the ball 
initial_flag = 1
while not rospy.is_shutdown():
	#turn everything of to begin with 
	if initial_flag==1:
		boat.set_throttle(0) 
		boat.set_angle(0) 
		initial_flag = 0
	else:	
		
		
		#proportion of the max propeller speed that the propeller should run at based on what the conveyor belt should be doing
		SPEEDS = {"on":.2, "lowered":.40, "unlowered":0.60}
		
		# find left to right posistion and distance to object 
		left_val, distance = vision.find_object_position()
		
		if left_val is None: 
		   print("can't find ball")
		   find_count = 0 
		   if search_count < 5: 
		      print("do nothing") 
		      search_count += 1
		   else:
		      search() 
		elif left_val == "camera": 
      		    print("add the webcam") 
		    break
		else:
		    search_count = 0 
		    if find_count < 5: 
			print("do nothing")
			find_count += 1 
		    else: 
		        angle = left_val * MAX_ANGLE
		        print("left_val:" + str(left_val))
		        print("distance:" + str(distance))

		        #stop it from correcting super slight angles
		        if abs(angle) < SIGNIFICANT_RUDDER_ANGLE:
			    angle = 0

		        if abs(angle - boat.angle) < SIGNIFICANT_RUDDER_ANGLE: 
			    print("keeping the angle the same") 

		        else: 
		           #move the rudder
		           boat.set_angle(angle, COMMENT)
			
		    if CONVEYOR_LOWER < distance:
			if not boat.throttle == MAX_THROTTLE*SPEEDS["unlowered"]:
			   boat.set_throttle(MAX_THROTTLE*SPEEDS["unlowered"], COMMENT)

		    elif CONVEYOR_ON < distance and distance < CONVEYOR_LOWER:
			if not boat.throttle == MAX_THROTTLE*SPEEDS["lowered"]:
			   boat.set_throttle(MAX_THROTTLE*SPEEDS["lowered"], COMMENT)
			boat.conveyor(False, True,COMMENT)

		    elif distance < CONVEYOR_ON:
			if not boat.throttle == MAX_THROTTLE*SPEEDS["on"]:
			   boat.set_throttle(MAX_THROTTLE*SPEEDS["on"],COMMENT)
			boat.conveyor(True,True,COMMENT)

		    else: #turn coneyor off 
			if not boat.throttle == 0:
			   boat.set_throttle(0)
			boat.conveyor(False,False,COMMENT)
