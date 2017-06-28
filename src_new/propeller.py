import rospy
from std_msgs.msg import Int8

class Propeller:
    def __init__(self,min_throttle, max_throttle):
        self.PROP_PUB_TOPIC = "motor_cmd/propeller"
        self.pub_prop = rospy.Publisher(self.PROP_PUB_TOPIC, Int8, queue_size=1)
        self.max_throttle = max_throttle
        self.min_throttle = min_throttle
        self.on = False
        self.throttle = min_throttle
        
    def set_throttle(self, throttle, comment=0):
        if throttle == 0:
            self.on = False
        else:
            self.on = True 
        if throttle > self.max_throttle:
            throttle = self.max_throttle
        elif throttle < self.min_throttle: 
            throttle = self.min_throttle
        if comment==1:
            print("setting throttle to {}" .format(throttle))
        self.pub_prop.publish(throttle)
        self.throttle = throttle
