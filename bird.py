import random

from sklearn.preprocessing import LabelBinarizer

from constants import *
from assets import *
from numpy import inf
from utils import random_nn_property
import numpy as np
from sklearn.neural_network import MLPClassifier


class Bird:
    ALIVE = 'alive'
    DEAD = 'dead'
    START_X = int(SCREENWIDTH * 0.2)
    START_Y = int((SCREENHEIGHT - 30) / 2)
    HIDDEN_LAYERS = (6,)
    ACTIVATION = 'identity'
    N_LAYERS = len(HIDDEN_LAYERS) + 1
    MUTATION_PROBABILTY = 0.9
    FLAP_PROBABILITY = 0.5
    MIN_PROPERY = -30
    MAX_PROPERY = -30

    def __init__(self,
                 index,
                 x=START_X,
                 y=START_Y,
                 vel_y=startVelY,
                 nn=MLPClassifier(hidden_layer_sizes=HIDDEN_LAYERS, activation=ACTIVATION)):
        self.index = index
        self.x = x
        self.y = random.uniform(0,BASEY)
        self.velY = vel_y
        self.flapped = False
        self.status = self.ALIVE
        self.score = 0
        self.rot = playerRot
        self.fitness = -inf
        self.nn = nn
        self.nn.n_outputs_ = 1
        self.nn.n_layers_ = self.N_LAYERS
        self.nn.out_activation_ = self.ACTIVATION
        self.random()

    def dead(self):
        self.status = self.DEAD

    def random(self):

        self.nn.coefs_=[
            # Matrix of first layer
            [
                # Weights for 1st input for each neuron
                [random_nn_property(), random_nn_property(), random_nn_property(), random_nn_property(), random_nn_property(), random_nn_property()],

                # Weights for 2nd input for each neuron
                [random_nn_property(), random_nn_property(), random_nn_property(), random_nn_property(), random_nn_property(), random_nn_property()],
            ],

            # Matrix of output weights (size of hidden layer)
            [
                [random_nn_property()],
                [random_nn_property()],
                [random_nn_property()],
                [random_nn_property()],
                [random_nn_property()],
                [random_nn_property()]
            ]
        ]

        self.nn.intercepts_ = [
            # Hidden layer biases
            [random_nn_property(), random_nn_property(), random_nn_property(), random_nn_property(), random_nn_property(), random_nn_property()],

            # Output bias
            [random_nn_property()]
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
        for i in xrange(0, self.N_LAYERS):
            #mutate weights
            for neuron in self.nn.coefs_[i]:
                for weight_index, weight in enumerate(neuron):
                    if random.uniform(0, 1) > self.MUTATION_PROBABILTY:
                        neuron[weight_index] = weight * random.uniform(-3,3)

            # mutate biases
            for bias_index, bias in enumerate(self.nn.intercepts_[i]):
                if random.uniform(0, 1) > self.MUTATION_PROBABILTY:
                    self.nn.intercepts_[i][bias_index] = bias * random.uniform(-3, 3)

    def crossover(self, bird):
        None

    def should_flap(self, distance_from_center, distance_to_next_pipe):
        print np.c_[
                np.array([distance_from_center]).ravel(),
                np.array([distance_to_next_pipe]).ravel()
           ]
        if self.nn.predict_proba(np.c_[
                np.array([distance_from_center]).ravel(),
                np.array([distance_to_next_pipe]).ravel()
           ])[0][0] > self.FLAP_PROBABILITY:
            self.flapped = True
            return True
        else:
            return False
