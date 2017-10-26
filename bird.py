import random
from constants import *

class Bird:

    def __init__(self, index, x, y, velY):
        self.index = index
        self.x = x
        self.y = y
        self.velY = velY
        self.flapped = False
        self.status = 'alive'
        self.score = 0
        self.rot = playerRot


    def mutate(self):
        None

    def flap(self):
        if random.random() > 0.9:
            self.flapped = True
            return True
        else:
            return False




