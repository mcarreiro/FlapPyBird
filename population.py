class Population:

    def __init__(self, birds):
        self.birds = birds

    def evolve(self):
        None

    def selection(self):
        None

    def alive(self):
        return filter(lambda x: x.status == 'alive', self.birds)