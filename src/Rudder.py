class Rudder:
    def __init__(self, max_angle, min_angle):
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.angle = 0
    def turn_rutter(self, angle):
        if angle < self.min_angle:
            angle = self.min_angle
        elif angle > self.max_angle:
            angle = self.max_angle 
        print("setting angle to {}" .format(angle))
        self.angle = angle