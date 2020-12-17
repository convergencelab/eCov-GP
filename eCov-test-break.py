'''
Author:     James Hughes
Date:       October 28, 2020

Version:    0.1


Change Log:
    0.1 (October 28, 2020): 
        - Initial version.

End Change Log

Similar to eCov-test, but this one will keep going and increase the connected-ness of the graphs. 

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
GRAPH_DIRECTORY = './../GRAPHS/sg_infectious_graphs/'
GRAPH_NAME = 'nonweightededges_2009_07_15.dat'
#GRAPH_TYPE = "DB15"

BETA = 0.09            # Spread Probability (25% works for Wendy graph)
GAMMA = 0.133           # Removal Probability. Based on 7 day, from sources
ALPHA = 6.4             # Latent period. Based on 6.4 days, from sources
INFECTED_0 = 0.02
GRAPH_SIZE = 500

# For ER graph
EDGE_p = 0.016
#EDGE_ps = [0.015, 0.016, 0.017, 0.018, 0.019, 0.020, 0.021, 0.022, 0.023, 0.024, 0.025, 0.026, 0.027, 0.028, 0.029, 0.030]
EDGE_ps = [0.031, 0.032, 0.033, 0.034, 0.035, 0.036, 0.037, 0.038, 0.039, 0.040, 0.041, 0.042, 0.043, 0.044, 0.045]

# For NWS graph
KNN = 10
REWIRE_p = 0.20
DROP = 1000
DROPs = [1100, 1000, 875, 750, 625, 500, 375, 250, 125, 0]
# for BA graph
#M = 3    
#Ms = [3, 4, 5, 6, 7, 8]
#Ms = [9, 10, 11, 12, 13, 14, 15]

# for BA graph
#M = 4    
#Ms = [3, 4, 5, 6, 7, 8]

# For PCG (Powerlaw Cluster Graph)
N_EDGES = 4
N_EDGESs = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
TRI_P = 0.66


ITERATIONS = 98
MEASURE_EVERY = 7
MITIGATIONS_PER_MEASURE = 30
ROLLOVER = False
#USE_ALL = False              ###########
USE_ALL = True              ###########
###########

# Testing Params
#OUTPUT_DIRECTORY = "./function_tests_break/"
OUTPUT_DIRECTORY = "./function_tests_use_all_break/"
N = 100
CHANGE_TOPOLOGY = True                     # CHANGE ME FOR STATIC/DYNAMIC
#FUNCTION = strategies.mitigation_degree5       # CHANGE ME FOR SWITCHING OUT FUNCTIONS

#functions = [strategies.mitigation_none, strategies.mitigation_random, strategies.mitigation_traveler, strategies.mitigation_degree5, strategies.mitigation_degree6, strategies.mitigation_degree7, strategies.mitigation_degree8, strategies.mitigation_degree9, strategies.mitigation_degree10, strategies.mitigation_all_F1]
#functions = [strategies.mitigation_none]
#functions = [strategies.mitigation_random]
#functions = [strategies.mitigation_all_F1]
#functions = [strategies.mitigation_all_F1, strategies.mitigation_random, strategies.mitigation_none]
functions = [strategies.mitigation_PCG_F1, strategies.mitigation_PCG_F2, strategies.mitigation_PCG_F3]


###########


#############
# Run Tests #
#############

# change this
#increases = EDGE_ps
#increases = DROPs
#increases = Ms
increases = N_EDGESs

for value in increases:
   
    for topology in [False, True]:
        CHANGE_TOPOLOGY = topology

        for strat in functions:
            FUNCTION = strat

            print("Function Being Tested:\t", FUNCTION.__name__)
            print("N Graph Topology:\t", CHANGE_TOPOLOGY)
            print("Break Value:\t\t", value)

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
                
                    #model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
                    
                    # ER
                    #model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, edge_p=value, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
                    #GRAPH_TYPE = "ER"
                   
                    # NWS
                    #model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, rewire_p=REWIRE_p, knn=KNN, alpha=ALPHA, drop=value, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
                    #GRAPH_TYPE = "NWS"

                    # BA
                    #model = snetwork.setup_network(size=GRAPH_SIZE, m=value, alpha=ALPHA, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
                    #GRAPH_TYPE = "BA"

                    # PCG
                    model = snetwork.setup_network(size=GRAPH_SIZE, n_edges=value, triangle_p=TRI_P, alpha=ALPHA, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
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


                # Evaluate the function
                # If we are doing the non mitigation 
                # we must not do a secondary strategy
                if FUNCTION.__name__ != "mitigation_none":
                    iterations, iterations_mitigations = evaluate.evaluate_individual(FUNCTION, m=model, traveler_set=travelers, mvc_set=minimal_vertex_cover, vert_avg_dist=vertex_average_distance, number_vertex_shortest=number_shortest_paths, Page_Rank=page_rank, Cluster_Coeff=cluster_coef, avg_degree=average_degree, short_dist=shortest_distances, avg_dist=average_distance, total_iterations=ITERATIONS, measure_every=MEASURE_EVERY, mitigations_per_measure=MITIGATIONS_PER_MEASURE, rollover=ROLLOVER, use_all=USE_ALL)
                else:
                    iterations, iterations_mitigations = evaluate.evaluate_individual(FUNCTION, m=model, traveler_set=travelers, mvc_set=minimal_vertex_cover, vert_avg_dist=vertex_average_distance, number_vertex_shortest=number_shortest_paths, Page_Rank=page_rank, Cluster_Coeff=cluster_coef, avg_degree=average_degree, short_dist=shortest_distances, avg_dist=average_distance, total_iterations=ITERATIONS, measure_every=MEASURE_EVERY, mitigations_per_measure=MITIGATIONS_PER_MEASURE, rollover=ROLLOVER, use_all=USE_ALL)

                # Bookkeeping
                all_iterations.append(iterations)
                all_iterations_mitigations.append(iterations_mitigations)
                
                #all_trends.append(model.build_trends(iterations))   
                #all_trends_mitigations.append(evaluate.mitigation_trends(iterations_mitigations))    

                


            ################
            # Save Results #
            ################

            print('Saving Results')

            pickle.dump((all_iterations, all_iterations_mitigations), open(os.path.join(OUTPUT_DIRECTORY, FUNCTION.__name__ + '_' + GRAPH_TYPE  + '_' + str(value) + '_' + str(CHANGE_TOPOLOGY)+'.pkl'),'wb'))

        # Quick hack to not run true on real graph
        if GRAPH_TYPE == "DB15":
            break

        



