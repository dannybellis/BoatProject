#Authors: Fiona Shyne and London Lowmanstone
import rospy
from std_msgs.msg import Int8

class Rudder:
    def __init__(self, min_angle, max_angle):
        self.RUDDER_PUB_TOPIC = "motor_cmd/steer"
        self.pub_rudder = rospy.Publisher(self.RUDDER_PUB_TOPIC, Int8, queue_size=1)
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.angle = 0
        
    def set_angle(self, angle,comment = 0):
        if angle < self.min_angle:
            angle = self.min_angle
        elif angle > self.max_angle:
            angle = self.max_angle 
        if comment == 1: 
            print("setting angle to {}" .format(angle))
        self.pub_rudder.publish(angle)
        self.angle = angle
