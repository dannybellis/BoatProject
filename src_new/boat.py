#Authors: Fiona Shyne and London Lowmanstone

from command_center import CommandCenter
from rudder import Rudder
from propeller import Propeller
from conveyor import Conveyor
from vision import Vision
from useful_functions import value_from_prop

class Boat:
    #conveyor_distance: distance to lower the conveyor
    #conveyor_on: distance to turn the conveyor on
    def __init__(self, conveyor_lower, conveyor_on, comment=0):
        self.RUDDER_MIN_ANGLE = -40
        self.RUDDER_MAX_ANGLE = 40
        self.PROPELLER_MIN_THROTTLE = -128
        self.PROPELLER_MAX_THROTTLE = 127
        self.VISION_FOCAL_LENGTH = 35 #mm
        self.VISION_OBJECT_WIDTH = 40 #mm
        self.CAMERA_PORT = 0
        #CommandCenter uses static methods, so we should not create an instance
        self.command_center = CommandCenter
        self.conveyor_lower = conveyor_lower
        self.conveyor_on = conveyor_on
        self.comment = comment
        self.rudder = Rudder(self.RUDDER_MIN_ANGLE, self.RUDDER_MAX_ANGLE, self.command_center)
        self.propeller = Propeller(self.PROPELLER_MIN_THROTTLE, self.PROPELLER_MAX_THROTTLE, self.command_center)
        self.conveyor = Conveyor()
        self.vision = Vision(self.CAMERA_PORT, self.VISION_FOCAL_LENGTH, self.VISION_OBJECT_WIDTH)

    # turns the motor based on the value is_left returns
    #TODO add in comment parameters
    def drive(self, comment=None):
        #default
        if comment is None:
            comment = self.comment
            
        #constants
        #the absolute value of the angle must be more than this in order for the rudder to be set to anything other than 0
        SIGNIFICANT_RUDDER_ANGLE = 0.1
        #proportion of the max propeller speed that the propeller should run at based on what the conveyor belt should be doing
        SPEEDS = {"on":.25, "lowered":.5, "unlowered":1}
            
        left_val, distance = self.vision.find_object_position()
        if left_val is None: 
            print("can't find ball")
        else:
            angle = value_from_prop(left_val, self.RUDDER_MIN_ANGLE, self.RUDDER_MAX_ANGLE)
            
            #stop it from correcting super slight angles
            if abs(angle) < SIGNIFICANT_RUDDER_ANGLE:
                angle = 0
            #move the rudder
            self.rudder.set_angle(angle)
        
            if self.conveyor_lower < distance:
                self.propeller.set_throttle(self.propeller.max_throttle*SPEEDS["unlowered"])
                
            elif self.conveyor_on < distance and distance < self.conveyor_lower:
                self.propeller.set_throttle(self.propeller.max_throttle*SPEEDS["lowered"])
                if self.conveyor.lowered == False: 
                    self.conveyor.lower()
                    
            elif distance < self.conveyor_on:
                self.propeller.set_throttle(self.propeller.max_throttle*SPEEDS["on"])
                if self.conveyor.on == False:
                    self.conveyor.turn_on()
                if self.conveyor.lowered == False: 
                    self.conveyor.lower()
                    
            else: #turn coneyor off 
                self.propeller.set_throttle(self.propeller.min_throttle)
                if self.conveyor.on == True: 
                    self.conveyor.turn_off()
                if self.conveyor.lowered == True: 
                    #raise the conveyor belt
                    self.conveyor.higher() 
            
            command = None   
            if not(command is None):
                print("running the following command {}".format(command))
                    