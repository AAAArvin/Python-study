import datetime
import random
import cairo

geneSet = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!."
target = "Genetic algorithm is a search algorithm used in computational mathematics to solve optimization."


def generate_parent(length):
    genes = []
    while len(genes) < length:
        sampleSize = min(length - len(genes), len(geneSet))
        genes.extend(random.sample(geneSet, sampleSize))
    return ''.join(genes)


def get_fitness(guess):
    return sum(1 for expected, actual in zip(target, guess) if expected == actual)


def mutate(parent):
    idx = random.randrange(0, len(parent))
    childGenes = list(parent)
    newGene, alternate = random.sample(geneSet, 2)
    childGenes[idx] = alternate if childGenes[idx] == newGene else newGene
    return ''.join(childGenes)


def display(guess, startTime):
    timeDiff = datetime.datetime.now() - startTime
    fitness = get_fitness(guess)
    WIDTH, HEIGHT = 1100, 50
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    ctx.set_font_size(20)
    ctx.move_to(5, 30)
    ctx.show_text(guess)
    name = "%02d" % fitness
    assert name
    surface.write_to_png("pic/"+name+".png")
    print("{}\t{}\t{}".format(guess, fitness, timeDiff))


random.seed()
startTime = datetime.datetime.now()
bestParent = generate_parent(len(target))
bestFitness = get_fitness(bestParent)
while True:
    child = mutate(bestParent)
    childFitness = get_fitness(child)
    if bestFitness >= childFitness:
        continue
    display(child, startTime)
    if childFitness >= len(bestParent):
        break
    bestFitness = childFitness
    bestParent = child