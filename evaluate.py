'''
Author:     James Hughes
Date:       June 8, 2020

Version:    0.8


Change Log:
    0.1 (June 8, 2020): 
        - Initial version.
        - Remove the use of global variabls

    0.2 (June 17, 2020):
        - Update to use new static measure of average graph degree

    0.3 (June 19, 2020):
        - Added more values to optimize (max infected, total infected)

    0.4 (July 15, 2020):
        - Added constants for node status
        - Fixed node status issue (had originally swapped exposed and infected)

    0.5 (July 24, 2020):
        - Commented out useless code for the do_we_mit function
        - Commented out old code from a previous version that is no longer needed (total infected, max infected)

    0.6 (August 17, 2020):
        - Use shortest distance measures

    0.7 (October 22, 2020):
        - Allow the system to apply a backup mitigation strategy if we have leftover mitigations
        - Default rule is to randomy apply (first come first serve), but can pass arbitrary function
        - This will be handy when doing the tests (eCov-test) because we will have a bunch of functions
        
    0.8 (April 26, 2021):
        - Added the option to make the graph dynamic
        - Simply added a few more params: a boolean, and add/remove probs
        

End Change Log


Fitness evaluation function and results/stats for throughout evolution


'''

###########
# Imports #
###########
import math
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import networkx as nx
import networkx.algorithms.community as comm
import numpy as np
import operator
import random


from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence

from measures import * 
from language import *

STATUS_SUSCEPTIBLE = 0
STATUS_EXPOSED = 2
STATUS_INFECTED = 1
STATUS_REMOVED = 3
STATUS_MITIGATED = 4





# default use all function is just random
def default_use_all(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        avg_degree,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        #i,
                        ):
    return True



######################
# Fitness Evaluation #
######################
   
# Fitness Function
def evaluate_individual(f, m, traveler_set, mvc_set=None, avg_degree=0, avg_dist=0, short_dist={}, vert_avg_dist=None, number_vertex_shortest=None, Page_Rank=None, Cluster_Coeff=None, total_iterations=0, measure_every=0, mitigations_per_measure=0, rollover=False, use_all=False, use_all_function=default_use_all, use_dynamic=False, ADD_p=0.00, REMOVE_p=0.00):

    max_infected = 0
    total_infected = 0
    total_mitigation = 0
    total_mitigation_effective = 0
    rollover_mitigations = 0
    

    # List to record network changes throughout simulation
    iterations = []
    
    # List to record network changes about mitigation strategies 
    iterations_mitigations = []

    if use_dynamic:
        GRAPH_SIZE= m.graph.graph.number_of_nodes()
        ADD = int(GRAPH_SIZE*ADD_p)
        REMOVE = int(GRAPH_SIZE*REMOVE_p)
        probs = [1/GRAPH_SIZE]*GRAPH_SIZE

    for i in range(total_iterations):

        # If it is a day we evaluate our network and apply mitigation
        if i != 0 and i % measure_every == 0:
            # Identify those that are able to hav emitigation applied
            # Remember, we pretend we do not know that exposed are exposed
            susceptible = get_all_of_status(m, target_status=STATUS_SUSCEPTIBLE)
            exposed = get_all_of_status(m, target_status=STATUS_EXPOSED)
            susexp = susceptible + exposed
            # Shuffle because we have limited resources and don't want any ordering
            random.shuffle(susexp)          
            infected = get_all_of_status(m, target_status=STATUS_INFECTED)

            
            num_suscept = get_num_nodes(m, STATUS_SUSCEPTIBLE)
            num_exposed = get_num_nodes(m, target_status=STATUS_EXPOSED)
            num_susexp = num_suscept + num_exposed
            num_infected = get_num_nodes(m, target_status=STATUS_INFECTED)
            num_removed = get_num_nodes(m, target_status=STATUS_REMOVED)

            #print(max_infected, '\t', total_infected, '\t', num_recovered - total_mitigation, '\t', total_mitigation)

            # Track mitigation details
            mitigations_used = 0
            mitigations_used_effective = 0
            mitigations_step = {}
            mitigations_step['iteration'] = i
            mitigations_step['status'] = {}
            mitigations_step['node_count'] = {}
            mitigations_step['status_delta'] = {}
            mitigations_step['total_mitigations'] = {}

            # Evaluate nodes
            # Only consider susceptible and exposed currently
            # In future, we could consider infected and do neighbour/ring mitigation
            for s in susexp:
                
                if mitigations_available(mitigations_per_measure + rollover_mitigations, mitigations_used):
                    node_status = get_status(m, s)
                    node_degree = get_degree(m, s)
                    avg_neighbour_degree = get_avg_neighbour_degree(m, s)
                    neighbour_susexp = get_num_neighbour_status(m, s, target_status=STATUS_SUSCEPTIBLE) + get_num_neighbour_status(m, s, target_status=STATUS_EXPOSED)
                    neighbour_infected = get_num_neighbour_status(m, s, target_status=STATUS_INFECTED) 
                    #neighbour_removed = get_num_neighbour_status(m, s, target_status=STATUS_REMOVED) 
                    traveler = is_traveler(traveler_set, s)
                    num_mitigation = mitigations_available(mitigations_per_measure + rollover_mitigations, mitigations_used)
                    #mitigation = get_cur_mitigations(mitigations_per_measure + rollover_mitigations, mitigations_used)

                    s_dist_inf = get_shortest_distance(short_dist, s, infected)

                    vertex_avg_dist = get_vertex_average_dist(vert_avg_dist, s)                     # vert_avg_dist
                    minimal_vertex_cover = is_in_min_cover(mvc_set, s)                              # MVX
                    num_vert_shortest = get_vertex_num_shortest_paths(number_vertex_shortest, s)    # num_short
                    page_rank = get_page_rank(Page_Rank, s)                                         # PR
                    cluster_coefficient =  get_cluster_coefficient(Cluster_Coeff, s)                # CCoef

                    do_we_mitigate = f(
                                        #node_status,
                                        node_degree,
                                        avg_neighbour_degree,
                                        neighbour_susexp, 
                                        neighbour_infected,
                                        #neighbour_removed,
                                        traveler,
                                        minimal_vertex_cover,
                                        avg_degree,
                                        avg_dist,
                                        vertex_avg_dist,
                                        #num_mitigation,
                                        #mitigation,
                                        num_susexp,
                                        num_infected,
                                        num_removed,
                                        num_vert_shortest,
                                        #s_dist_inf,
                                        page_rank,
                                        cluster_coefficient,
                                        #i,
                                        )

                    if do_we_mitigate:
                        if node_status == STATUS_SUSCEPTIBLE:
                            cur_num_mitigated = mitigate_self(m, s)
                            mitigations_used += cur_num_mitigated
                            mitigations_used_effective += cur_num_mitigated
                            mitigations_step['status'][s] = STATUS_MITIGATED

                        # Apply mitigation to exposed, but this wastes mitigation                        
                        else:
                            mitigations_used += 1
                       
                else:
                    break

            ########################################################
            # Make it so have an option to use all the mitigations
            if use_all:
                # Basically repeat above with the given strategy
                # but figure out suscept again since they could've changed
                #
                susceptible = get_all_of_status(m, target_status=STATUS_SUSCEPTIBLE)
                susexp = susceptible + exposed
                # Shuffle because we have limited resources and don't want any ordering
                random.shuffle(susexp)     

                # These numbers may have changed too
                num_suscept = get_num_nodes(m, STATUS_SUSCEPTIBLE)
                num_susexp = num_suscept + num_exposed
                num_removed = get_num_nodes(m, target_status=STATUS_REMOVED)

                # Evaluate nodes
                # Only consider susceptible and exposed currently
                # In future, we could consider infected and do neighbour/ring mitigation
                for s in susexp:
                    
                    if mitigations_available(mitigations_per_measure + rollover_mitigations, mitigations_used):
                        node_status = get_status(m, s)
                        node_degree = get_degree(m, s)
                        avg_neighbour_degree = get_avg_neighbour_degree(m, s)
                        neighbour_susexp = get_num_neighbour_status(m, s, target_status=STATUS_SUSCEPTIBLE) + get_num_neighbour_status(m, s, target_status=STATUS_EXPOSED)
                        neighbour_infected = get_num_neighbour_status(m, s, target_status=STATUS_INFECTED) 
                        #neighbour_removed = get_num_neighbour_status(m, s, target_status=STATUS_REMOVED) 
                        traveler = is_traveler(traveler_set, s)
                        num_mitigation = mitigations_available(mitigations_per_measure + rollover_mitigations, mitigations_used)
                        #mitigation = get_cur_mitigations(mitigations_per_measure + rollover_mitigations, mitigations_used)

                        s_dist_inf = get_shortest_distance(short_dist, s, infected)

                        do_we_mitigate = use_all_function(
                                            #node_status,
                                            node_degree,
                                            avg_neighbour_degree,
                                            neighbour_susexp, 
                                            neighbour_infected,
                                            #neighbour_removed,
                                            traveler,
                                            avg_degree,
                                            #avg_dist,
                                            #num_mitigation,
                                            #mitigation,
                                            num_susexp,
                                            num_infected,
                                            num_removed,
                                            #s_dist_inf,
                                            #i,
                                            )

                        if do_we_mitigate:
                            if node_status == STATUS_SUSCEPTIBLE:
                                cur_num_mitigated = mitigate_self(m, s)
                                mitigations_used += cur_num_mitigated
                                mitigations_used_effective += cur_num_mitigated
                                mitigations_step['status'][s] = STATUS_MITIGATED

                            # Apply mitigation to exposed, but this wastes mitigation                        
                            else:
                                mitigations_used += 1
                           
                    else:
                        break
            #############################################


            # If we are rolloig over
            # Rollover should be after the use_all 
            # since the backup strategy may have leftovers
            if rollover:
                # rollovers can accumulate over multiple periods
                rollover_mitigations = (mitigations_per_measure + rollover_mitigations) - mitigations_used





            total_mitigation += mitigations_used
            total_mitigation_effective += mitigations_used_effective

            mitigations_step['node_count'][STATUS_MITIGATED] = total_mitigation_effective
            mitigations_step['status_delta'][STATUS_MITIGATED] = mitigations_used_effective
            mitigations_step['total_mitigations']['total'] = mitigations_used
            mitigations_step['total_mitigations']['effective'] = mitigations_used_effective
            mitigations_step['total_mitigations']['ineffective'] = mitigations_used - mitigations_used_effective

            iterations_mitigations.append(mitigations_step)

        #current_infected = get_num_nodes(m, target_status=STATUS_INFECTED)
        #total_infected += current_infected
        #max_infected = max(max_infected, current_infected)

        iterations.append(m.iteration())
        
        
        # HERE WE DO DYNAMIC STUFF!!!!!!!!     
        if use_dynamic:
            adds = select_group(m.graph.graph, ADD, probs)
            removes = select_group(m.graph.graph, REMOVE, probs)
        
            # Apply the changes
            for v in adds:
                add_edge(m.graph.graph,v)
            
            for v in removes:
                remove_edge(m.graph.graph,v)
        
        

    #final_num_susceptible = get_num_nodes(m)    
    #final_num_removed = get_num_nodes(m, target_status=STATUS_REMOVED)

    # Use this between chromosome evals
    # Will reset network with same params
    # BUT, the same nodes will NOT start infected
    # Would this make more sense in evaluate_population?
    m.reset()

    #print(max_infected, '\t', total_infected, '\t', final_num_removed - total_mitigation, '\t', total_mitigation)
    #print(final_num_removed, total_mitigation, final_num_removed - total_mitigation)
    #return final_num_removed - total_mitigation, 
    #return total_infected, 
    # Maybe I will incorporate vaccines in here somehow later
    #return final_num_susceptible,
    #return final_num_susceptible, total_mitigation
    return iterations, iterations_mitigations,

def mitigation_trends(iterations_mitigations):
    trends = [{'trends': {}}]

    trends[0]['trends']['node_count'] = {'total':[], 'effective':[], 'ineffective':[]}
    trends[0]['trends']['status_delta'] = {'total':[], 'effective':[], 'ineffective':[]}

    running_total = 0
    running_effective = 0
    running_ineffective = 0

    for iteration in iterations_mitigations:

        current_total = iteration['total_mitigations']['total']
        current_effective = iteration['total_mitigations']['effective']
        current_ineffective = iteration['total_mitigations']['ineffective']

        running_total += current_total
        running_effective += current_effective
        running_ineffective += current_ineffective
        
        trends[0]['trends']['node_count']['total'].append(running_total)
        trends[0]['trends']['node_count']['effective'].append(running_effective)
        trends[0]['trends']['node_count']['ineffective'].append(running_ineffective)

        trends[0]['trends']['status_delta']['total'].append(current_total)
        trends[0]['trends']['status_delta']['effective'].append(current_effective)
        trends[0]['trends']['status_delta']['ineffective'].append(current_ineffective)
    
    return trends



def convert_iterations(iterations, m):
    trends = m.build_trends(iterations)
    final_susceptible = iterations[-1]['node_count'][STATUS_SUSCEPTIBLE]
    final_removed = iterations[-1]['node_count'][STATUS_REMOVED]
    max_infected = max(trends[0]['trends']['node_count'][STATUS_INFECTED])
    total_infected = sum(trends[0]['trends']['node_count'][STATUS_INFECTED])  # Area under curve 
    return final_susceptible, max_infected, total_infected, final_removed, 

def convert_iterations_mitigations(iterations_mitigations):
    trends = mitigation_trends(iterations_mitigations)
    total = trends[0]['trends']['node_count']['total'][-1]
    effective = trends[0]['trends']['node_count']['effective'][-1]
    ineffective = trends[0]['trends']['node_count']['ineffective'][-1]
    
    return total, effective, ineffective, 



def remove_edge(g, v):
    neighbour = select_neighbour(g, v)
    g.remove_edge(v, neighbour)
    
    # If we accidentally disconnected the graph
    # UNDO UNDO UNDO
    # If this happens, we just skip and don't bother trying again because v may only have
    # 1 neighbour and I am lazy
    if not(nx.has_path(g,v,neighbour)):
        g.add_edge(v, neighbour)
        #try_again = remove_edge(g, neighbour)
        return False #or try_again #, neighbour
    return True #, neighbour

# Two potential problems here:
# 1. If the neighbour has no other neighbours other than v, then we get an exception. If this happens, ignore and plug our nose
# 2. If v already has an edge to neighbour_neighbour, then just plug our nose and ignore
def add_edge(g, v):
    neighbour = select_neighbour(g, v)
    try:
        neighbour_neighbour = select_neighbour_neighbour(g, neighbour, v)
        g.add_edge(v, neighbour_neighbour)
        return True
    except ValueError:
        # If nothing works, just add a random fucking
        # edge. Sure, maybe the random vertex selected
        # is already connected, but whatever, better than nothing
        planB = np.random.randint(g.number_of_nodes())
        g.add_edge(v, planB)
        return False
    

        return False

# Select however many verticies for a 
# group (add, remove, change). 
def select_group(g, n, ps):
    group = []
    for i in range(n):
        v = np.random.choice(range(g.number_of_nodes()), p=ps)
        group.append(v)
    return group

# Generate the vertices probabilities    
def generate_node_prob(g):
    edge_counts = []
    
    # Get each vertex's neighbour count 
    for v in range(g.number_of_nodes()):
        edge_counts.append(len(list(g.neighbors(v))))
        
    # Normalize neighbour count for probabilities
    edge_counts = np.array(edge_counts)
    edge_counts_p = edge_counts/np.sum(edge_counts)
    
    return edge_counts_p
    # select vertex probabilistically 
    #individual = np.random.choice(range(GRAPH_SIZE, p=edge_counts_p)
    #return individual    

def select_neighbour(g, v):
    neighbours = list(g.neighbors(v))
    neighbour = np.random.choice(neighbours)
    return neighbour

    
def select_neighbour_neighbour(g, v, ex):
    # get this vertex's neighbour list
    # remove ex from it
    candidates = list(g.neighbors(v))
    candidates.remove(ex)
    while True:
        neighbour = np.random.choice(candidates)
        # If the neighbour neighbour is not the original vertex
        # DONE
        # Oterwise
        # Try again, but remove this neighbour from the possibilities
        # NOTE: if we ever run out of neighbours, we give up
        if not ex in list(g.neighbors(neighbour)):
            break
        else:
            candidates.remove(neighbour)

    return neighbour    


