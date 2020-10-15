'''
Author:     James Hughes
Date:       May 22, 2020

Version:    0.12

Change Log:
    0.1: 
        - Initial version.
        - Built from code from eCov-GP. 

    0.2:
        - New function to execute individual population members on an SEIR model. 

    0.3 (May 28, 2020):
        - Update to the evaluate_individual function to return lists of dictionaries for node changes and mitigation changes
        - Mitigation trends function
        - Functions to convert trends and iterations to simple summary numbers (more useful for GP itself)

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

    0.8 (June 19, 2020):
        - Small change to allow the new average degree measure

    0.9 (July 22, 2020):
        - Updated alpha to reflect the latent period, NOT a probability

    0.10 (September 3, 2020):
        - Change parameters and model creation
        - Update to include new static measures (average degree, average distance)

    0.11 (September 12, 2020):
        - Print average results for fitness
        - Print arg mins/maxs for fitnesses

    0.11 (September 17, 2020):
        - Print best 5 for total infected over time metric (this assumes we have this metric as the last element in the objectives)

End Change Log

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
RESULTS_NAME = "09-30-2020_03-44-01.pkl"

# Graph & Disease
GRAPH_DIRECTORY = './../GRAPHS/sg_infectious_graphs/'
GRAPH_NAME = 'nonweightededges_2009_07_15.dat'

BETA = 0.09            # Spread Probability (25% works for Wendy graph)
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

# for BA graph
M = 3    

ITERATIONS = 140        
MEASURE_EVERY = 7
MITIGATIONS_PER_MEASURE = 20
ROLLOVER = True

##################
# Epidemic Setup #
##################


model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
# ER
#model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, edge_p=EDGE_p, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
# NWS
#model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, rewire_p=REWIRE_p, knn=KNN, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
# BA
#model = snetwork.setup_network(size=GRAPH_SIZE, m=M, alpha=ALPHA, beta=BETA, gamma=GAMMA, infected=INFECTED_0)

# Identify Static Whole Graph Measures
travelers = get_travelers(model)
average_degree = get_average_degree(model)
shortest_distances = get_shortest_distances_all_nodes(model)
average_distance = get_avg_distances_all_nodes(model)

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




###############################
# Visualize Results as Trees  #
###############################

def draw_tree(ind):
    nodes, edges, labels = gp.graph(ind)

    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    pos = graphviz_layout(g, prog="dot")

    nx.draw_networkx_nodes(g, pos)
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_labels(g, pos, labels)
    plt.show()

os.environ['PATH'] = os.environ['PATH']+';'+os.environ['CONDA_PREFIX']+r"\Library\bin\graphviz"

#draw_tree(population[0])


# List to keep track of all results
# will print out averages and arg mins
all_results = []

for i in range(len(population)): 
    print(i, population[i].fitness)
    all_results.append(list(population[i].fitness.getValues()))
    #draw_tree(population[i])

# Print summary stats
all_results = np.array(all_results)

print()
print("mean, median")
print(all_results.mean(axis=0))
print(np.median(all_results,axis=0))
print()

print("min, arg min")
print(all_results.min(axis=0))
print(all_results.argmin(axis=0))
print("Best 5", np.argsort(all_results[:,-1])[:5])

print()
print("max, arg max")
print(all_results.max(axis=0))
print(all_results.argmax(axis=0))
print("Best 5", np.argsort(all_results[:,-1])[-6:])

########################
# Run on SEIR network  #
########################

def no_mit(a,b,c,d,e,f):
    return False

def diffusion_trend(ind):
    iterations, iterations_mitigations = evaluate.evaluate_individual(toolbox.compile(ind), m=model, traveler_set=travelers, avg_degree=average_degree, short_dist=shortest_distances, avg_dist=average_distance, total_iterations=ITERATIONS, measure_every=MEASURE_EVERY, mitigations_per_measure=MITIGATIONS_PER_MEASURE, rollover=ROLLOVER)
    trends = model.build_trends(iterations)
    # Visualization
    viz = DiffusionTrend(model, trends)
    viz.plot()
    viz = DiffusionPrevalence(model, trends)
    viz.plot()
    return iterations, trends


#diffusion_trend(population[0])

