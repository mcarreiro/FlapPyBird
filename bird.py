import random
from constants import *
from assets import *
from numpy import inf
import numpy as np
from sklearn.neural_network import MLPClassifier


class Bird:
    ALIVE = 'alive'
    DEAD = 'dead'
    START_X = int(SCREENWIDTH * 0.2)
    START_Y = int((SCREENHEIGHT - 30) / 2)

    def __init__(self,
                 index,
                 x=START_X,
                 y=START_Y,
                 vel_y=startVelY,
                 nn=MLPClassifier(hidden_layer_sizes=(6,), activation='logistic', max_iter=500, random_state=0, warm_start=True)):
        self.index = index
        self.x = x
        self.y = y
        self.velY = vel_y
        self.flapped = False
        self.status = self.ALIVE
        self.score = 0
        self.rot = playerRot
        self.fitness = -inf
        self.nn = nn
        self.nn.n_outputs_ = 1
        self.nn.n_layers_ = 2
        self.nn.out_activation_ = 'logistic'
        self.random()

    def dead(self):
        self.status = self.DEAD

    def random(self):

        self.nn.coefs_=[
            # Matrix
            [
                # Weights for 1st input for each neuron
                [random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5)],

                # Weights for 2nd input for each neuron
                [random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5)],
            ],

            # Matrix of output weights (size of hidden layer)
            [
                [random.uniform(-5, 5)],
                [random.uniform(-5, 5)],
                [random.uniform(-5, 5)],
                [random.uniform(-5, 5)],
                [random.uniform(-5, 5)],
                [random.uniform(-5, 5)]
            ]
        ]

        self.nn.intercepts_ = [
            # Hidden layer biases
            [random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5)],

            # Output bias
            [random.uniform(-5, 5)]
        ]


    def is_alive(self):
        return self.status == self.ALIVE

    def revive(self):
        self.status = self.ALIVE
        self.score = 0
        self.x = self.START_X
        self.y = self.START_Y
        self.velY = startVelY

    def mutate(self):
        self.revive()

    def crossover(self, bird):
        None

    def should_flap(self, distance_from_center, distance_to_next_pipe):
        print self.nn.predict_proba(np.c_[
                np.array([distance_from_center]).ravel(),
                np.array([distance_to_next_pipe]).ravel()
           ])
        if self.nn.predict_proba(np.c_[
                np.array([distance_from_center]).ravel(),
                np.array([distance_to_next_pipe]).ravel()
           ])[0][0] > 0.5:
            self.flapped = True
            return True
        else:
            return False
