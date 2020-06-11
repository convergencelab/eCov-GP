'''
Author:     James Hughes
Date:       June 11, 2020

Version:    0.1


Change Log:
    0.1 (June 11, 2020): 
        - Initial version.
    
End Change Log

Generate a collection of results for a given function. This will be used to generate statistics to really evaluate the strategy effectivness

'''

###########
# Imports #
###########
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import networkx as nx
import networkx.algorithms.community as comm
import numpy as np
import os
import pickle

from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence

from measures import * 

import evaluate
import snetwork
import strategies


###########
# PARAMS  #
###########

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

# Testing Params
OUTPUT_DIRECTORY = "./function_tests/"
N = 100
CHANGE_TOPOLOGY = False
FUNCTION = strategies.mitigation_none

###########





#############
# Run Tests #
#############

print('Beginning Testing')

all_iterations = []
all_iterations_mitigations = []

all_trends = []
all_trends_mitigations = []


for i in range(N):

    # Reporting
    if i % (0.1 * N) == 0:
        print(i/N)

    # If this is the first run OR we want to change the topology all the time
    if i == 0 or CHANGE_TOPOLOGY:
        model = snetwork.setup_network(size=GRAPH_SIZE, edge_p=EDGE_p, alpha=ALPHA, beta=BETA, gamma=GAMMA, infected=INFECTED_0)

        # Identify travelers
        travelers = get_travelers(model)


    # Evaluate the function
    iterations, iterations_mitigations = evaluate.evaluate_individual(FUNCTION, m=model, traveler_set=travelers, total_iterations=ITERATIONS, measure_every=MEASURE_EVERY, mitigations_per_measure=MITIGATIONS_PER_MEASURE, rollover=ROLLOVER)

    # Bookkeeping
    all_iterations.append(iterations)
    all_iterations_mitigations.append(iterations_mitigations)
    
    #all_trends.append(model.build_trends(iterations))   
    #all_trends_mitigations.append(evaluate.mitigation_trends(iterations_mitigations))    

    


################
# Save Results #
################

print('Saving Results')

pickle.dump((all_iterations, all_iterations_mitigations), open(os.path.join(OUTPUT_DIRECTORY, FUNCTION.__name__ + '.pkl'),'wb'))



