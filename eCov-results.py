'''
Author:     James Hughes
Date:       May 22, 2020

Version:    0.7

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
SUB_DIRECTORY = "good/25_50_500_140_20/"
RESULTS_NAME = "05-26-2020_03-14-31.pkl"

# Graph & Disease
GRAPH_DIRECTORY = './../../GRAPHS/'
GRAPH_NAME = 'github_notop.dat'
BETA = 0.025            # Spread Probability
GAMMA = 0.133           # Incubation Probability. Based on 7 day, from sources
ALPHA = 0.175           # Recovery Probability. Based on 5.2 days, from sources
INFECTED_0 = 0.01
GRAPH_SIZE = 500
EDGE_p = 0.04
ITERATIONS = 140        
MEASURE_EVERY = 7
MITIGATIONS_PER_MEASURE = 20
ROLLOVER = True

##################
# Epidemic Setup #
##################


model = snetwork.setup_network(size=GRAPH_SIZE, edge_p=EDGE_p, alpha=ALPHA, beta=BETA, gamma=GAMMA, infected=INFECTED_0)

# Identify travelers
travelers = get_travelers(model)

############
# GP Setup #
############

toolbox, mstats, logbook = sgp.setup_gp(language, evaluate.evaluate_individual, m=model, traveler_set=travelers, total_iterations=ITERATIONS, measure_every=MEASURE_EVERY, mitigations_per_measure=MITIGATIONS_PER_MEASURE, rollover=ROLLOVER)

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

draw_tree(population[0])


for i in range(len(population)): 
    print(i, population[i].fitness)
    #draw_tree(population[i])




########################
# Run on SEIR network  #
########################

def diffusion_trend(ind):
    iterations, iterations_mitigations = evaluate.evaluate_individual(toolbox.compile(ind), m=model, traveler_set=travelers, total_iterations=ITERATIONS, measure_every=MEASURE_EVERY, mitigations_per_measure=MITIGATIONS_PER_MEASURE, rollover=ROLLOVER)
    trends = model.build_trends(iterations)
    # Visualization
    viz = DiffusionTrend(model, trends)
    viz.plot()
    viz = DiffusionPrevalence(model, trends)
    viz.plot()
    return iterations, trends


#diffusion_trend(population[0])

