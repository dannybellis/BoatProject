#Authors: Fiona Shyne and London Lowmanstone

import time

#prints time of section of code
class Timer:
    def __init__ (self, name):
        self.name = name
    def __enter__(self):
        self.start = time.time()
    def __exit__(self,*excs):
        print("{} Time:{}".format(self.name, time.time() - self.start))