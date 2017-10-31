from population import Population


class PopulationFactory:

    def __init__(self):
        pass

    @classmethod
    def create_random_population(cls, size):
        return Population(size)
