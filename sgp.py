'''
Author:     James Hughes
Date:       June 9, 2020

Version:    0.1


Change Log:
    0.1 (June 9, 2020): 
        - Initial version.
  
End Change Log

setup the GP stuff


'''

###########
# Imports #
###########

import numpy as np
import operator



from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp


def setup_gp(language, eval_function, **kwargs):

    toolbox = base.Toolbox()

    # Magic code to make it parallel?
    # Must be run like this though:
    #   ipython -m scoop eCov-GP.py
    from scoop import futures
    toolbox.register("map", futures.map)


    creator.create("FitnessMin", base.Fitness, weights=(-1,))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

    toolbox.register("expr", gp.genHalfAndHalf, pset=language, min_=1, max_=4)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=language)

    # Operators
    #toolbox.register("evaluate", evaluate.evaluate_individual, m=model, traveler_set=travelers, total_iterations=ITERATIONS, measure_every=MEASURE_EVERY, mitigations_per_measure=MITIGATIONS_PER_MEASURE, rollover=ROLLOVER)
    toolbox.register("evaluate", eval_function, **kwargs)
    toolbox.register("elitism", tools.selBest, k=1)
    toolbox.register("select", tools.selTournament, tournsize=2)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=language)

    ## Bloat rules 
    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=5))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=5))

    toolbox.decorate("mate", gp.staticLimit(key=len, max_value=32))
    toolbox.decorate("mutate", gp.staticLimit(key=len, max_value=32))

    # Statistics Bookkeeeping
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", np.mean)
    mstats.register("std", np.std)
    mstats.register("min", np.min)
    mstats.register("max", np.max)

    logbook = tools.Logbook()


    return toolbox, mstats, logbook

