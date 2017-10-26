from bird import Bird
from assets import *
from constants import *

from population import Population


class PopulationFactory:

    def __init__(self):
        pass

    @classmethod
    def create_random_population(cls, size):
        players = []
        for x in xrange(size):
            players.append(
                Bird(x,
                     int(SCREENWIDTH * 0.2),
                     int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2),
                     startVelY
                     )
            )
        return Population(players)
