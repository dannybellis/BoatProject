class Propeller:
    def __init__(self, max_throttle, min_throttle):
        self.max_throttle = max_throttle
        self.min_throttle = min_throttle
        self.on = False
        self.throttle = min_throttle
    def set_throttle(self, throttle):
        if throttle == self.min_throttle:
            self.on = False
        else:
            self.on = True 
        print("setting throttle to {}" .format(throttle))
        self.throttle = throttle