from bird import Bird
from numpy import inf
import random

class Population:

    GOOD_THRESHOLD = -inf

    def __init__(self, size):
        self.birds = []
        self.size = size
        self.create_generation()

    def next_generation(self):
        # new generation
        new_birds = []

        # best of the best
        selection = self.selection()

        # All selection to the next generation
        new_birds.extend(selection)

        # crossover 6
        random.choice(selection)

        self.birds = new_birds

    def create_generation(self):
        for i in xrange(self.size):
            self.birds.append(Bird(i))

    def selection(self):
        good_birds = filter(lambda x: x.fitness > self.GOOD_THRESHOLD, self.birds)
        ordered = sorted(good_birds, key=lambda x: x.fitness, reverse=True)

        #Best of their generation
        return ordered[:int(0.4*self.size)]

    def alive(self):
        return filter(lambda x: x.is_alive(), self.birds)