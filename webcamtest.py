#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import *


cam = cv2.VideoCapture(0)
ret,frame = cam.read()
if frame is None: 
	print("cam is not working") 
else: 
	print("cam is working")
	print(frame)
