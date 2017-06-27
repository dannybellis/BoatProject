#Authors: Fiona Shyne and London Lowmanstone

class Conveyor:
    def __init__(self):
        self.lowered = False
        self.on = False
        
    def turn_on(self, comment=0):
        if comment == 1:
            print("turning conveyor on")
        self.on = True
        
    def turn_off(self, comment=0):
        if comment == 1:
            print("turning conveyor off")
        self.on = False
        
    def lower(self, comment=0):
        if comment == 1:
            print("lowering conveyor")
        self.lowered = True
        
    def higher(self, comment=0):
        if comment == 1:
            print("rasing conveyor")
        self.lowered = False
