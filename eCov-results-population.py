'''
Author:     James Hughes
Date:       November 23, 2020

Version:    0.3

Change Log:
    0.1 (November 23, 2020): 
        - Initial version.
        - Built from code from eCov-results. 

    0.2 (December 4, 2020):
        - Have it be the same 10 graphs for each, that way we do not need to do 10*x, where x is the number of candidates
        - This may not be ideal for randomness, but way faster, soooo deal 

    0.3 (December 4, 2020):
        - I undid the idea from v0.2
        - Turns out the randomless really will be important
            * Remember, I wanna' know how good they are in general, not how good they are on the same 10 graphs
            
End Change Log

Since there is such variability in strategy effectivness due to changes in graph topoloty and/or starting conditions, we need to evaluate all models on a number of graphs...


'''

###########
# Imports #
###########

import math
import matplotlib.pyplot as plt
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import networkx as nx
import networkx.algorithms.community as comm
import numpy as np
import operator
import os
import pickle
import random

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence

from networkx.drawing.nx_agraph import graphviz_layout

from measures import * 
from language import *


import evaluate
import sgp
import snetwork

###########
# PARAMS  #
###########

RESULTS_DIRECTORY = "./output/"
SUB_DIRECTORY = ""
RESULTS_NAME = "12-03-2020_01-42-29.pkl"

# Graph & Disease-
GRAPH_DIRECTORY = './../GRAPHS/sg_infectious_graphs/'
GRAPH_NAME = 'nonweightededges_2009_07_15.dat'

BETA = 0.09             # Spread Probability (25% works for Wendy graph)
GAMMA = 0.133           # Removal Probability. Based on 7 day, from sources
ALPHA = 6.4             # Latent period. Based on 6.4 days, from sources
INFECTED_0 = 0.02
GRAPH_SIZE = 500

# For ER graph
EDGE_p = 0.016

# For NWS graph
KNN = 10
REWIRE_p = 0.20
DROP = 1000

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

# Graphs to Test on
N_GRAPHS = 10


##################
# Epidemic Setup #
##################


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

vertex_average_distance = get_node_avg_distances_all_nodes(model)
minimal_vertex_cover = get_min_vertex_cover(model)
number_shortest_paths = get_node_number_shortest_paths(model)
page_rank = get_all_page_rank(model)
cluster_coef = clustering_coefficient(model)

############
# GP Setup #
############

toolbox, mstats, logbook = sgp.setup_gp(language, evaluate.evaluate_individual, m=model, traveler_set=travelers, avg_degree=average_degree, short_dist=shortest_distances, avg_dist=average_distance, total_iterations=ITERATIONS, measure_every=MEASURE_EVERY, mitigations_per_measure=MITIGATIONS_PER_MEASURE, rollover=ROLLOVER)

#############
# File I/O  #
#############

results = pickle.load(open(os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, RESULTS_NAME), 'rb'))

population = results["population"]
logbook = results["logbook"]



########################
# Evaluate on X graphs #
########################

# Turn the population into functions to be evaluated
compiled_pop = list(map(toolbox.compile, population))

# List to hold onto results to be saved
all_results = []

for i, f in enumerate(compiled_pop):
#for i in range(5):
    FUNCTION = f
    #FUNCTION = compiled_pop[i]
    print(population[50])
    # Dict to hold results
    results = {}
    results['sus'] = []
    results['max_inf'] = []
    results['tot_inf'] = []
    results['rem'] = []
    results['tot_mit'] = []
    results['eff_mit'] = []
    results['ine_mit'] = []

    for _ in range(N_GRAPHS):

        #model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
                    
        # ER
        #model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, edge_p=EDGE_p, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
        #GRAPH_TYPE = "ER"
                   
        # NWS
        #model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, rewire_p=REWIRE_p, knn=KNN, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
        #GRAPH_TYPE = "NWS"

        # BA
        #model = snetwork.setup_network(size=GRAPH_SIZE, m=M, alpha=ALPHA, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
        #GRAPH_TYPE = "BA"

        # PCG
        model = snetwork.setup_network(size=GRAPH_SIZE, n_edges=N_EDGES, triangle_p=TRI_P, alpha=ALPHA, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
        GRAPH_TYPE = "PCG"

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

        terations, iterations_mitigations = evaluate.evaluate_individual(FUNCTION, m=model, traveler_set=travelers, mvc_set=minimal_vertex_cover, vert_avg_dist=vertex_average_distance, number_vertex_shortest=number_shortest_paths, Page_Rank=page_rank, Cluster_Coeff=cluster_coef, avg_degree=average_degree, short_dist=shortest_distances, avg_dist=average_distance, total_iterations=ITERATIONS, measure_every=MEASURE_EVERY, mitigations_per_measure=MITIGATIONS_PER_MEASURE, rollover=ROLLOVER, use_all=USE_ALL)

        final_susceptible, max_infected, total_infected, final_removed = evaluate.convert_iterations(terations, model)
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
oFile = open(os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, RESULTS_NAME[:-4] + '-population-results.csv'), 'w')

for r in all_results:
    sus = np.median(r['sus'])
    max_inf = np.median(r['max_inf'])
    tot_inf = np.median(r['tot_inf'])
    rem = np.median(r['rem'])
    tot_mit = np.median(r['tot_mit'])
    eff_mit = np.median(r['eff_mit'])
    ine_mit = np.median(r['ine_mit'])

    oFile.write(str(sus) + ', ' + str(max_inf) + ', ' + str(tot_inf) + ', ' + str(rem) + ', ' + str(tot_mit) + ', ' + str(eff_mit) + ', ' + str(ine_mit) + '\n')

oFile.close()



