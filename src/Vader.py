class Vader:
    def __init__(self):
        self.lowered = False
        self.on = False
    def turn_on(self):
        print("turning vader on")
        self.on = True
    def turn_off(self):
        print("turning vader off")
        self.on = False
    def lower(self):
        print("lowering vader")
        self.lowered = True
    def higher(self):
        print("rasing vader")
        self.lowered = False