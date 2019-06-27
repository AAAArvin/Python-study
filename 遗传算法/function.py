import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class GA(object):
    def __init__(self, DNA_SIZE, POP_SIZE, CROSS_RATE, MUTATION_RATE, N_GENERATIONS, X_BOUND):
        self.DNA_size = DNA_SIZE
        self.pop_size = POP_SIZE
        self.cross_rate = CROSS_RATE
        self.mutate_rate = MUTATION_RATE
        self.generations = N_GENERATIONS
        self.bounds = X_BOUND
        self.populations = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))

    def fitness(self, y):
        return y + 1e-3 - np.min(y)

    def crossover(self, parent, pop):
        if np.random.rand() < self.cross_rate:
            i_ = np.random.randint(0, self.pop_size, size=1)
            cross_points = np.random.randint(0, 2, self.DNA_size).astype(np.bool)
            parent[cross_points] = pop[i_, cross_points]
        return parent

    def mutate(self, child):
        for point in range(self.DNA_size):
            if np.random.rand() < self.mutate_rate:
                child[point] = 1 if child[point] == 0 else 0
        return child

    def select(self, pop, fit):
        idx = np.random.choice(np.arange(self.pop_size), size=self.pop_size, replace=True, p=fit/fit.sum())
        return pop[idx]

    def translateDNA(self, pop):
        return np.dot(pop, 2 ** np.arange(self.DNA_size)[::-1]) / float(2 ** self.DNA_size - 1) * self.bounds[1]

    def F(self, x):
        return np.sin(10 * x) * x + np.cos(2 * x) * x


if __name__ == '__main__':
    ga = GA(DNA_SIZE=10, POP_SIZE=100, CROSS_RATE=0.8, MUTATION_RATE=0.03, N_GENERATIONS=200, X_BOUND=[0, 5])
    fig = plt.figure()  # something about plotting
    x = np.linspace(*ga.bounds, 200)
    plt.plot(x, ga.F(x))
    fit_DNA = []
    ims = []
    for _ in range(ga.generations):
        F_values = ga.F(ga.translateDNA(ga.populations))
        sca = plt.scatter(ga.translateDNA(ga.populations), F_values, s=200, lw=0, c='red', alpha=0.5).findobj()
        ims.append(sca)
        fit = ga.fitness(F_values)
        fit_DNA.append(ga.translateDNA(ga.populations[np.argmax(fit), :]))
        ga.populations = ga.select(ga.populations, fit)
        pop_copy = ga.populations.copy()
        for parent in ga.populations:
            child = ga.crossover(parent, pop_copy)
            child = ga.mutate(child)
            parent[:] = child
    ani = animation.ArtistAnimation(fig, ims, interval=200, repeat_delay=1000)
    ani.save("test1.gif", writer='pillow')
    print('最大值自变量x=', max(fit_DNA))
    print('最大值y=', ga.F(max(fit_DNA)))