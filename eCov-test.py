'''
Author:     James Hughes
Date:       June 11, 2020

Version:    0.1


Change Log:
    0.1 (June 11, 2020): 
        - Initial version.
    
End Change Log

Generate a collection of results for a given function. This will be used to generate statistics to really evaluate the strategy effectivness.

'''

###########
# Imports #
###########

import os
import pickle


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
CHANGE_TOPOLOGY = True                     # CHANGE ME FOR STATIC/DYNAMIC
FUNCTION = strategies.mitigation_F1       # CHANGE ME FOR SWITCHING OUT FUNCTIONS

###########


#############
# Run Tests #
#############

print("Function Being Tested:\t", FUNCTION.__name__)
print("Dynamic Graph Topology:\t", CHANGE_TOPOLOGY)

all_iterations = []
all_iterations_mitigations = []

all_trends = []
all_trends_mitigations = []


print('Beginning Testing')

for i in range(N):

    # Reporting
    if i % (0.1 * N) == 0:
        print(i/N)

    # If this is the first run OR we want to change the topology all the time
    if i == 0 or CHANGE_TOPOLOGY:
    
        #print("\tMaking New Graph")
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

pickle.dump((all_iterations, all_iterations_mitigations), open(os.path.join(OUTPUT_DIRECTORY, FUNCTION.__name__ + '_' + str(CHANGE_TOPOLOGY) +'.pkl'),'wb'))



