'''
Author:     James Hughes
Date:       May 22, 2020

Version:    0.16

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

    0.12 (September 17, 2020):
        - Print best 5 for total infected over time metric (this assumes we have this metric as the last element in the objectives)

    0.13 (November 24, 2020):
        - Added a function to investigate whole population batch results 

    0.14 (November 25, 2020):
        - new function, save_function 
            * We can just dump the function out and load it up in another place (strategies)

    0.15 (January 4, 2021):
        - Printed out the top results automatically

    0.16 (January 11, 2021):
        - Changed such that it will iterate over all relevant files in a specificed directory

End Change Log

'''

###########
# Imports #
###########

import csv
import dill
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
SUB_DIRECTORY = "January-14-CC_USE_ALL/"

# This is the CC results 
# I believe there were two diff runs here, but I do not know which was what and what I did different...
#RESULTS_NAME = "12-19-2020_14-15-56.pkl" # 792 [ 134.  2689.5] 968[ 127. 2774.]
#RESULTS_NAME = "12-19-2020_14-44-34.pkl" # 376 [ 133. 2691.] 
#RESULTS_NAME = "12-19-2020_15-24-34.pkl" # crap
#RESULTS_NAME = "12-19-2020_15-33-40.pkl" # 659 [ 134. 2706.]
#RESULTS_NAME = "12-19-2020_17-18-23.pkl" # 57 [ 131.  2678.5]

#RESULTS_NAME = "12-19-2020_17-33-30.pkl" # crap
#RESULTS_NAME = "12-19-2020_17-51-47.pkl" # 705 [ 127. 2704.] 
#RESULTS_NAME = "12-19-2020_18-13-16.pkl" # 602 [ 128.5 2771.5]
#RESULTS_NAME = "12-19-2020_18-21-29.pkl" # 496 [ 132. 2602.] 434 [ 133. 2607.] 708 [ 129. 2677.] 
#RESULTS_NAME = "12-19-2020_18-38-20.pkl" # crap

# 2nd batch
#RESULTS_NAME = "12-20-2020_11-47-01.pkl" # 631 [ 131. 2580.] 	768 [ 126.5 2660. ] (all results are good)
#RESULTS_NAME = "12-20-2020_12-47-41.pkl" # 616 [ 130.  2666.5]
#RESULTS_NAME = "12-20-2020_13-39-31.pkl" # 158 [ 129. 2570.]
#RESULTS_NAME = "12-20-2020_14-32-58.pkl" # 957 [ 125. 2538.]
#RESULTS_NAME = "12-20-2020_14-39-48.pkl" # 212 [ 130.5 2614. ] 527 [ 129.5 2617. ]

#RESULTS_NAME = "12-20-2020_15-17-51.pkl" # 356 [ 126. 2594.]
#RESULTS_NAME = "12-20-2020_16-07-22.pkl" # meh
#RESULTS_NAME = "12-20-2020_16-32-10.pkl" # 13 [ 128.5 2445.5] *************************
#RESULTS_NAME = "12-20-2020_16-53-56.pkl" # meh
#RESULTS_NAME = "12-20-2020_17-26-30.pkl" # 75 [ 123.  2785.5]


# This was Late DEC Old Desktop
#RESULTS_NAME = "12-20-2020_18-52-14.pkl" # (484) 125, 2877
#RESULTS_NAME = "12-20-2020_19-39-56.pkl" # (336) 133.5, 2711.5 (617) 127, 2775 (887)125.5, 2871.
#RESULTS_NAME = "12-20-2020_19-53-42.pkl" # (601) 129, 2787
#RESULTS_NAME = "12-20-2020_19-57-25.pkl" # (36) 129, 2886 (478) 123.5, 2688 (669) 130, 2734
#RESULTS_NAME = "12-20-2020_20-02-41.pkl" # 145 [ 128.5 2745. ]
#RESULTS_NAME = "12-20-2020_20-06-19.pkl" # crap
#RESULTS_NAME = "12-20-2020_20-21-53.pkl" # crap
#RESULTS_NAME = "12-20-2020_20-45-42.pkl" # crap


#RESULTS_NAME = "12-08-2020_10-36-23.pkl" # 105 2471.5
#RESULTS_NAME = "12-08-2020_13-20-06.pkl" # 109.5 2680
#RESULTS_NAME = "12-08-2020_14-40-36.pkl" # 114.5 2542.5
#RESULTS_NAME = "12-08-2020_15-36-04.pkl" # 112.5 2654
#RESULTS_NAME = "12-08-2020_15-40-26.pkl" # 111 2532.5
#RESULTS_NAME = "12-08-2020_15-48-28.pkl" # 110.5 2528
#RESULTS_NAME = "12-08-2020_18-17-53.pkl" # 107.5 2584.5
#RESULTS_NAME = "12-08-2020_20-28-39.pkl" # 110 2600.5



#SUB_DIRECTORY = "December-Generation_500"
#RESULTS_NAME = "12-02-2020_23-55-14.pkl" # good
#RESULTS_NAME = "12-03-2020_00-29-14.pkl" # ok
#RESULTS_NAME = "12-03-2020_01-18-07.pkl" # meh
#RESULTS_NAME = "12-03-2020_01-18-21.pkl" # ok
#RESULTS_NAME = "12-03-2020_01-27-56.pkl" # meh
#RESULTS_NAME = "12-03-2020_01-28-17.pkl" # ok
#RESULTS_NAME = "12-03-2020_01-31-23.pkl" # good
#RESULTS_NAME = "12-03-2020_01-42-29.pkl" # less than good, better than meh


#########################################################
# Functions for looking at data and pop summary results #
#########################################################

def load_population_results(RESULTS_DIRECTORY, SUB_DIRECTORY, RESULTS_NAME):
    pRes = csv.reader(open(os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, RESULTS_NAME[:-4] + '-population-results.csv'), 'r'))
    pRes = np.array(list(pRes)).astype(float)
    return pRes


def print_summary(results):
    print()
    print("mean, median")
    print(results.mean(axis=0))
    print(np.median(results,axis=0))
    print()

    print("min, arg min")
    print(results.min(axis=0))
    print(results.argmin(axis=0))
    print("Best 5 MI", np.argsort(results[:,0])[:10])
    
    for i in np.argsort(results[:,0]):
        if results[i, 0] < 120 and results[i, -1] < 2600:
            print('\t\t\t\t\t\t', end='')
            print(i, end='')
            print(results[i])


    #print("max, arg max")
    #print(results.max(axis=0))
    #print(results.argmax(axis=0))
    #print("Best 5 MI ", np.argsort(results[:,0])[-6:])
    print()

    #print("min, arg min")
    #print(results.min(axis=0))
    #print(results.argmin(axis=0))
    print("Best 5 TI", np.argsort(results[:,-1])[:10])

    for i in np.argsort(results[:,-1]):
        if results[i, -1] < 2500:
            print('\t\t\t\t\t\t', end='')
            print(i, end=' ')
            print(results[i])

    #print("max, arg max")
    #print(results.max(axis=0))
    #print(results.argmax(axis=0))
    #print("Best 5 TI ", np.argsort(results[:,-1])[-6:])

    print()
    print('min again')
    print(results.min(axis=0))
    print(results.argmin(axis=0))

def save_function(pop, i, RESULTS_DIRECTORY, SUB_DIRECTORY, RESULTS_NAME):
    # Turn the population into functions to be evaluated
    compiled_ind = toolbox.compile(pop[i])
    print(compiled_ind)
    string_compiled_ind = dill.dumps(compiled_ind)
    print(string_compiled_ind)
    oFileName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, RESULTS_NAME[:-4] + '_' + str(i) + '-compiled.dill')
    dill.dump(compiled_ind, open(oFileName, 'wb'))
    #pickle.dump(string_compiled_ind, open(oFileName, 'w'))
    #pickle.dump(compiled_ind, open(oFileName, 'w'))

###############################
# Visualize Results as Trees  #
###############################

def draw_tree(ind):
    # Print out text version of tree
    print(ind)
    
    # Drawing stuff
    # Couldn't get this working on Windows :( 
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

########################
# Run on SEIR network  #
########################

def no_mit(a,b,c,d,e,f):
    return False

def diffusion_trend(ind):
    iterations, iterations_mitigations = evaluate.evaluate_individual(toolbox.compile(ind), m=model, traveler_set=travelers, mvc_set=minimal_vertex_cover, vert_avg_dist=vertex_average_distance, number_vertex_shortest=number_shortest_paths, Page_Rank=page_rank, Cluster_Coeff=cluster_coef, avg_degree=average_degree, short_dist=shortest_distances, avg_dist=average_distance, total_iterations=ITERATIONS, measure_every=MEASURE_EVERY, mitigations_per_measure=MITIGATIONS_PER_MEASURE, rollover=ROLLOVER, use_all=USE_ALL)
    trends = model.build_trends(iterations)
    # Visualization
    viz = DiffusionTrend(model, trends)
    viz.plot()
    viz = DiffusionPrevalence(model, trends)
    viz.plot()
    return iterations, trends


def get_specific_file_results(RESULTS_DIRECTORY, SUB_DIRECTORY, RESULTS_NAME):
    results = pickle.load(open(os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, RESULTS_NAME), 'rb'))

    population = results["population"]
    logbook = results["logbook"]


    # List to keep track of all results
    # will print out averages and arg mins
    all_results = []

    '''
    for i in range(len(population)): 
        print(i, population[i].fitness)
        all_results.append(list(population[i].fitness.getValues()))
        #draw_tree(population[i])
    '''
    # Print summary stats
    #all_results = np.array(all_results)
    #print_summary(all_results)
    
    print('***** File: ' + RESULTS_NAME + ' *****')

    # Results gen from ...-population
    pop_res = load_population_results(RESULTS_DIRECTORY, SUB_DIRECTORY, RESULTS_NAME)
    pop_res = pop_res[:, [1,2]]
    print_summary(pop_res)
    
    return population

#diffusion_trend(population[0])



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

# For PCG (Powerlaw Cluster Graph)
N_EDGES = 4
TRI_P = 0.66
#############################

ITERATIONS = 140        
MEASURE_EVERY = 7
MITIGATIONS_PER_MEASURE = 20
ROLLOVER = False
USE_ALL = False
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

for fPath in os.scandir(os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY)):
    if fPath.path.endswith(".pkl"):
        print(fPath.path)
        RESULTS_DIRECTORY = "./output/"
        SUB_DIRECTORY = SUB_DIRECTORY
        RESULTS_NAME = fPath.name

        the_pop = get_specific_file_results(RESULTS_DIRECTORY, SUB_DIRECTORY, RESULTS_NAME)
        print()
        print()
        







