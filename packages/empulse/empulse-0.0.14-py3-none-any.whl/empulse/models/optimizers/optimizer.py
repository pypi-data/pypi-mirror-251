


class Optimizer(ABC):

    @abstractmethod
    def optimize(self, func, bounds):
        pass


class RGA(Optimizer):

    def __init__(self):
        self.population = []

    def evolve(self):
        yield self.select_best()
        while True:
            self.crossover()
            self.mutate()
            self.select()
            yield self.select_best()

    def optimize(self, func, bounds):
        ...

    def crossover(self):
        ...

    def mutate(self):
        ...

    def select(self):
        ...

    def select_best(self):
        ...
