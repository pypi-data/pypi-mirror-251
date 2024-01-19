class ProfLogitClassifier:

    def __init__(self, objective):
        self.objective = objective


if __name__ == '__main__':
    from itertools import takewhile, islice
    from ..optimizers.optimizer import RGA

    def objective():
        ...



    def optimize(objective):
        optimizer = RGA()
        run_n_iterations = lambda data, n: islice(optimizer.optimize(data), n)
        run_until_convergence = lambda data, threshold: takewhile(
            lambda x: x.rel_improvement < threshold, optimizer.optimize(data)
        )

        run_n_iterations()

