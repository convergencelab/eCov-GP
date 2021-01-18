'''
Author:     James Hughes
Date:       December 4, 2020

Version:    0.2


Change Log:
    0.1 (December 4, 2020): 
        - Initial version.
    
    0.2 (December 15, 2020):
        - Made it so we use the same N_GRAPHS (eg. 30) to validate all strategies
        - Perhaps not ideal, but a lot lot lot lot faster to do it this way 
            * N_GRAPHS applied to 1000 vs N_GRAPHS * 1000

End Change Log

Combine eCov-GP and the results-population such that we get the results and the validated results all in one shot

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
POPULATION = 1000
GENERATIONS = 750
CROSSOVER = 0.8
MUTATION = 0.1

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
        #ind.fitness.values = (final_susceptible, total_mitigations, max_infected, total_infected, )
        #ind.fitness.values = (final_susceptible, )
        ind.fitness.values = (max_infected, total_infected, )


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

# Phase PCG Phase 2 add
vertex_average_distance = get_node_avg_distances_all_nodes(model)
minimal_vertex_cover = get_min_vertex_cover(model)
number_shortest_paths = get_node_number_shortest_paths(model)
page_rank = get_all_page_rank(model)
cluster_coef = clustering_coefficient(model)

############
# GP Setup #
############

toolbox, mstats, logbook = sgp.setup_gp(language, evaluate.evaluate_individual, m=model, traveler_set=travelers, mvc_set=minimal_vertex_cover, vert_avg_dist=vertex_average_distance, number_vertex_shortest=number_shortest_paths, Page_Rank=page_rank, Cluster_Coeff=cluster_coef, avg_degree=average_degree, short_dist=shortest_distances, avg_dist=average_distance, total_iterations=ITERATIONS, measure_every=MEASURE_EVERY, mitigations_per_measure=MITIGATIONS_PER_MEASURE, rollover=ROLLOVER, use_all=USE_ALL)


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
RESULTS_NAME = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + '.pkl'
pickle.dump(results, open(os.path.join(RESULTS_DIRECTORY, RESULTS_NAME),'wb'))


################
# evalpop here #
################


# Graphs to Test on
N_GRAPHS = 50

########################
# Evaluate on X graphs #
########################

# Turn the population into functions to be evaluated
compiled_pop = list(map(toolbox.compile, population))

# List to hold onto results to be saved
all_results = []

# This is where we will store the N_GRAPHS and their details
# This will use the same N_GRAPHS for each candidate solution
# This may not be ideal, but it'll be AAA LLLOOOTTT faster
# Besides, this is validation anyways 

models_measures = {}
models_measures['graph'] = []
models_measures['travelers'] = []
models_measures['average_degree'] = []
models_measures['shortest_distances'] = []
models_measures['average_distance'] = []
models_measures['vertex_average_distance'] = []
models_measures['minimal_vertex_cover'] = []
models_measures['number_shortest_paths'] = []
models_measures['page_rank'] = []
models_measures['cluster_coef'] = []

# Generate the N_GRAPHS and store them
for _ in range(N_GRAPHS):

    #model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
                
    # ER
    #model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, edge_p=EDGE_p, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
               
    # NWS
    #model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, rewire_p=REWIRE_p, knn=KNN, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)


    # BA
    #model = snetwork.setup_network(size=GRAPH_SIZE, m=M, alpha=ALPHA, beta=BETA, gamma=GAMMA, infected=INFECTED_0)

    # PCG
    model = snetwork.setup_network(size=GRAPH_SIZE, n_edges=N_EDGES, triangle_p=TRI_P, alpha=ALPHA, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
    models_measures['graph'].append(model)


    # Identify Static Whole Graph Measures
    models_measures['travelers'].append(get_travelers(model))
    models_measures['average_degree'].append(get_average_degree(model))
    models_measures['shortest_distances'].append(get_shortest_distances_all_nodes(model))
    models_measures['average_distance'].append(get_avg_distances_all_nodes(model))

    # Phase PCG Phase 2 add
    models_measures['vertex_average_distance'].append(get_node_avg_distances_all_nodes(model))
    models_measures['minimal_vertex_cover'].append(get_min_vertex_cover(model))
    models_measures['number_shortest_paths'].append(get_node_number_shortest_paths(model))
    models_measures['page_rank'].append(get_all_page_rank(model))
    models_measures['cluster_coef'].append(clustering_coefficient(model))


for i, f in enumerate(compiled_pop):
#for i in range(5):
    print(i)
    FUNCTION = f
    #FUNCTION = compiled_pop[i]
    #print(population[50])
    # Dict to hold results
    results = {}
    results['sus'] = []
    results['max_inf'] = []
    results['tot_inf'] = []
    results['rem'] = []
    results['tot_mit'] = []
    results['eff_mit'] = []
    results['ine_mit'] = []

    for j in range(N_GRAPHS):

        model = models_measures['graph'][j]


        # Identify Static Whole Graph Measures
        travelers = models_measures['travelers'][j]
        average_degree = models_measures['average_degree'][j]
        shortest_distances = models_measures['shortest_distances'][j]
        average_distance = models_measures['average_distance'][j]

        # Phase PCG Phase 2 add
        vertex_average_distance = models_measures['vertex_average_distance'][j]
        minimal_vertex_cover = models_measures['minimal_vertex_cover'][j]
        number_shortest_paths = models_measures['number_shortest_paths'][j]
        page_rank = models_measures['page_rank'][j]
        cluster_coef = models_measures['cluster_coef'][j]

        iterations, iterations_mitigations = evaluate.evaluate_individual(FUNCTION, m=model, traveler_set=travelers, mvc_set=minimal_vertex_cover, vert_avg_dist=vertex_average_distance, number_vertex_shortest=number_shortest_paths, Page_Rank=page_rank, Cluster_Coeff=cluster_coef, avg_degree=average_degree, short_dist=shortest_distances, avg_dist=average_distance, total_iterations=ITERATIONS, measure_every=MEASURE_EVERY, mitigations_per_measure=MITIGATIONS_PER_MEASURE, rollover=ROLLOVER, use_all=USE_ALL)

        final_susceptible, max_infected, total_infected, final_removed = evaluate.convert_iterations(iterations, model)
        total_mitigations, effective_mitigations, ineffective_mitigations = evaluate.convert_iterations_mitigations(iterations_mitigations)

        results['sus'].append(final_susceptible)
        results['max_inf'].append(max_infected)
        results['tot_inf'].append(total_infected)
        results['rem'].append(final_removed)
        results['tot_mit'].append(total_mitigations)
        results['eff_mit'].append(effective_mitigations)
        results['ine_mit'].append(ineffective_mitigations)
        


    all_results.append(results)



# Save Results
print('\nSaving Results')
oFile = open(os.path.join(RESULTS_DIRECTORY, RESULTS_NAME[:-4] + '-population-results.csv'), 'w')

for r in all_results:
    print(r['sus'])
    print(r['max_inf'])
    print(r['tot_inf'])
    print(r['rem'])
    print(r['tot_mit'])
    print(r['eff_mit'])
    print(r['ine_mit'])
    sus = np.median(r['sus'])
    max_inf = np.median(r['max_inf'])
    tot_inf = np.median(r['tot_inf'])
    rem = np.median(r['rem'])
    tot_mit = np.median(r['tot_mit'])
    eff_mit = np.median(r['eff_mit'])
    ine_mit = np.median(r['ine_mit'])

    oFile.write(str(sus) + ', ' + str(max_inf) + ', ' + str(tot_inf) + ', ' + str(rem) + ', ' + str(tot_mit) + ', ' + str(eff_mit) + ', ' + str(ine_mit) + '\n')

oFile.close()


