'''
Author:     James Hughes
Date:       May 19, 2020

Version:    0.14


Change Log:
    0.1 (May 19, 2020): 
        - Initial version.
    
    0.2 (May 22, 2020):
        - Remove the end visualization.
        - Save final results to pickled file.
        - Visualization and results interpretation will occur in separate script. 

    0.3 (May 28, 2020):
        - 'evaluate_individual' returns the iterations list generated by ndlib's 'iterate'
        - Create and return an iterations like thing for mitigations (it will be some weird dictionary)
        - Use the trends function from nblib to convert the iterations list into something usable
        - Create a trends like function to convert the iterations like thing for mitigations into something usable for the fitness values

    0.4 (May 30, 2020):
        - Add a boolean flag to allow unused mitigations to be used at next evaluation period

    0.5 (June 3, 2020):
        - Evaluate Individual can take a chromosome that needs to be compiled, or an individual function. 

    0.6 (June 8, 2020):
        - Evaluate Individual takes a function
        - Evaluate population now passes a compiled function to evaluate individual

    0.7 (June 8, 2020):
        - Split files into sub-files of logical units
        - Files will be imported 

    0.8 (June 17, 2020):
        - Small changes to system to allow for new measure (average degree)

    0.9 (June 19, 2020):
        - Added more values to optimize (max infected, total infected)

    0.10 (July 22, 2020):
        - Updated alpha to reflect the latent period, NOT a probability

    0.11 (July 29, 2020):
        - Turn eleitism back on since we are recalculating everyone's fitness anyways

    0.12 (August 17, 2020):
        - Incorporating shortest dist stuff (new graph measure)

    0.13 (September 1, 2020):
        - Remove the casting as a dict

    0.14 (October 26, 2020):
        - Added the use all flag to make it so we use the secondary strategy

    0.15 (November 12, 2020):
        - Added the option to have PCG (the best random graph so far). 
        - This addition will only include chanes for Phase 1 of runs 
            * No new measures; keep similar for easy comparison. 

End Change Log


Run with this: ipython -m scoop eCov-GP.py


A GP search for effective vaccination strategies for a given graph

This version is relatively simple:
- Will be single objective. 
    - Will probably eventually want to make multi
        - Min tree size
        - Min max infected
        - Integral under infected curve
        - Total infected over period
        - Min mitigation used
- SEIR model (no E', where E' is exposed AND infected, but not detected)
- No fancy node info (age, pre existing conditions, etc.)
- Simple graph statistics 
    - Static
        - Travelers (CURRENT VERSION HAS A VERY HACK-IE IMPLEMENTATION)
    - Whole Graph
        - Number of certain status
        - Number of mitigations used
        - Is mitigation available? (boolean)
        - ***** (REMOVED FOR THIS VERSION DUE TO TIME CONSTRAINTS) Average distance between nodes of a given status
    - Single/Local Measures
        - Current Status
        - Node Degree
        - Average degree of neighbours
        - is traveler? (boolean)
        - Get number of neighbours of certain status

- Atomic Heuristics
    - For Susceptible & Exposed
        - Mitigate Self
    - For Infected
        - Mitigate Neighbours (ring vaccination)
    - MIGHT only work on susceptible/exposed (no looking at ring vaccination yet) 

I think to start the trees will simply be a boolean expression. If true, vac, otherwise, no. 

'''

# Can use this ipython -m scoop eCov-GP.py

###########
# Imports #
###########
import csv
import datetime
import itertools
import math
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import networkx as nx
import networkx.algorithms.community as comm
import numpy as np
import operator
import os
import pickle
import random
import sys

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence

from measures import * 
from language import *

import evaluate
import sgp
import snetwork

###########
# PARAMS  #
###########

# GP System
DATA_DIRECTORY = "./"
RESULTS_DIRECTORY = "./output/"
DATA_NAME = ""
POPULATION = 500
GENERATIONS = 500
CROSSOVER = 0.8
MUTATION = 0.15

# Graph & Disease
GRAPH_DIRECTORY = './../GRAPHS/sg_infectious_graphs/'
GRAPH_NAME = 'nonweightededges_2009_07_15.dat'

# SEIR Params
BETA = 0.09            # Spread Probability (25% works for Wendy graph)
GAMMA = 0.133           # Removal Probability. Based on 7 day, from sources
ALPHA = 6.4             # Latent period. Based on 6.4 days, from sources
INFECTED_0 = 0.02

#############################
# RANDOM GRAPH PARAMS BELOW #
#############################
GRAPH_SIZE = 500

# For ER graph
EDGE_p = 0.016

# For NWS graph
KNN = 10
REWIRE_p = 0.20
DROP = 1000

# for BA graph
M = 4    

# For PCG (Powerlaw Cluster Graph)
N_EDGES = 4
TRI_P = 0.66
#############################

ITERATIONS = 98
MEASURE_EVERY = 7
MITIGATIONS_PER_MEASURE = 30
ROLLOVER = False
USE_ALL = False
###########


# How to evaluate the whole population 
# Calls stuff from evaluate 
def evaluate_population(pop):
    # Only worry about individuals with INVALID fitness values
    # This will save some time
    #invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    #fitnesses = list(map(toolbox.evaluate, invalid_ind))
    compiled_pop = list(map(toolbox.compile, pop))
    fitnesses = list(map(toolbox.evaluate, compiled_pop))
    #for ind, fit in zip(invalid_ind, fitnesses):
    for ind, fit in zip(pop, fitnesses):
        # DO NOT FORGET TO UNPACK THE DICTS WITH TEENDS AND WHATNOT!!!!!
        final_susceptible, max_infected, total_infected, final_removed = evaluate.convert_iterations(fit[0], model)
        total_mitigations, effective_mitigations, ineffective_mitigations = evaluate.convert_iterations_mitigations(fit[1])
        ind.fitness.values = (final_susceptible, total_mitigations, max_infected, total_infected, )
        #ind.fitness.values = (final_susceptible, )


##################
# Epidemic Setup #
##################

# Load custom graph
#model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
# ER
#model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, edge_p=EDGE_p, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
# NWS
#model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, rewire_p=REWIRE_p, knn=KNN, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
# BA
#model = snetwork.setup_network(size=GRAPH_SIZE, m=M, alpha=ALPHA, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
# PCG
model = snetwork.setup_network(size=GRAPH_SIZE, n_edges=N_EDGES, triangle_p=TRI_P, alpha=ALPHA, beta=BETA, gamma=GAMMA, infected=INFECTED_0)


# Identify Static Whole Graph Measures
travelers = get_travelers(model)
average_degree = get_average_degree(model)
shortest_distances = get_shortest_distances_all_nodes(model)
average_distance = get_avg_distances_all_nodes(model)

############
# GP Setup #
############

toolbox, mstats, logbook = sgp.setup_gp(language, evaluate.evaluate_individual, m=model, traveler_set=travelers, avg_degree=average_degree, short_dist=shortest_distances, avg_dist=average_distance, total_iterations=ITERATIONS, measure_every=MEASURE_EVERY, mitigations_per_measure=MITIGATIONS_PER_MEASURE, rollover=ROLLOVER, use_all=USE_ALL)


#######################
# Evolutionary Search #
#######################

population = toolbox.population(n=POPULATION)

print('Starting Evolution')
for g in range(GENERATIONS):

    if g % (0.1 * GENERATIONS) == 0:
        print(g/GENERATIONS)

    evaluate_population(population)
    record = mstats.compile(population)
    logbook.record(gen=g, **record)
    
    # Elitism
    best = toolbox.elitism(population)  # For elitism
    best_clone = toolbox.clone(best)
    
    # Selection
    offspring = toolbox.select(population, len(population)-1)   # For elitism
    #offspring = toolbox.select(population, len(population))    # for NOT elitism
    offspring_clone = list(map(toolbox.clone, offspring))
        
    # Simplified genetic operators 
    new_population = algorithms.varAnd(offspring_clone, toolbox, CROSSOVER, MUTATION)

    # replace the population with the new population
    population[:] = best_clone + new_population        # For elitism
    #population[:] = new_population                     # for NOT elitism

    
print('Ending Evolution')

evaluate_population(population)
record = mstats.compile(population)
logbook.record(gen=GENERATIONS, **record)


logbook.header = "gen", "fitness", "size"
logbook.chapters["fitness"].header = "min", "avg", "max"
logbook.chapters["size"].header = "min", "avg", "max"

print(logbook)


################
# Save Results #
################

print('Saving Results')
results = dict(population=population, logbook=logbook)
pickle.dump(results, open(os.path.join(RESULTS_DIRECTORY, datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + '.pkl'),'wb'))

# plot difftrend so it doesn't crash because of SCOOP
#iterations, iterations_mitigations = evaluate.evaluate_individual(toolbox.compile(population[0]), m=model, traveler_set=travelers, avg_degree=average_degree, total_iterations=ITERATIONS, measure_every=MEASURE_EVERY, mitigations_per_measure=MITIGATIONS_PER_MEASURE, rollover=ROLLOVER)
#trends = model.build_trends(iterations)
# Visualization
#viz = DiffusionTrend(model, trends)
#viz.plot()

# Exit so the SCOOP doesn't try to run again and crash 
#sys.exit()

