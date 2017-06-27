#Authors: Fiona Shyne and London Lowmanstone

class Rudder:
    def __init__(self, min_angle, max_angle ,command_center):
        self.command_center = command_center
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
        self.command_center.do("rudder", angle)
        self.angle = angle
