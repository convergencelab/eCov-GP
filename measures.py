'''
Author:     James Hughes
Date:       June 8, 2020

Version:    0.2


Change Log:
    0.1 (June 8, 2020): 
        - Initial version

    0.2 (June 17, 2020):
        - Added average degree static graph measure
    


End Change Log

All graph measures are contained within this file. 

New measures will be added here.

Not all measures will necessairly be used


'''

###########
# Imports #
###########

import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import networkx as nx
import networkx.algorithms.community as comm
import numpy as np
import random

from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence

###########################
# Graph Measure Functions #
###########################

# STATIC MEASURES #

# Find nodes that connect communities
def get_travelers(model):

    # Pick some node in a community
    com_nodes = [list(x)[0] for x in comm.greedy_modularity_communities(model.graph.graph)]
    all_travelers = set()

    # Find minimal cut edges to seperate communities
    ## Really this is a bad hack, but whatever. 
    for i in range(len(com_nodes)):
        for j in range(i+1, len(com_nodes)):        
            travelers = nx.minimum_edge_cut(model.graph.graph, com_nodes[i], com_nodes[j])
            
            # add the nodes from the edges to a set
            for t in travelers:
                all_travelers.add(t[0])
                all_travelers.add(t[1])

    return all_travelers

# Get thje average degree of the graph
def get_average_degree(model):
    d = []

    for n in range(len(model.graph.graph.nodes)):
        d.append(model.graph.graph.degree(n))

    return np.average(d)


# WHOLE GRAPH MEASURES #

# Get all nodes of a certain status
# NOTE: We may want to return those that are susceptible AND exposed
#       Since in reality we don't know who is who
def get_all_of_status(model, target_status=0):
    targets = []
    for node, status in model.status.items():
        if status == target_status:
            targets.append(node)
    return targets

# Number of nodes of current status
def get_num_nodes(model, target_status=0):
    return list(model.status.values()).count(target_status) 


# Number of mitigations currently available
def get_cur_mitigations(total, used):
    return total - used

def mitigations_available(total, used):
    return (total - used) > 0

# Average distance between nodes
def get_avg_dist_between_nodes(model, nodes, proportion=1.0):

    # Get a random subset of the nodes baseed on the
    # proportion of nodeswe will consider in our sample
    nodes = random.sample(nodes, int(len(nodes)*proportion))

    # add all the distances to this list
    # in the end we will average these values    
    distances = []

    # Only calc the top right triangle of distances
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            distances.append(nx.shortest_path_length(model.graph.graph, nodes[i], nodes[j]))

    # If there are no distances to take an average of
    if len(distances) < 1:
        avg = 0
    else:
        avg = np.average(distances)

    # return the average
    return avg

# SINGLE GRAPH MEASUREOUTPUT_DIRECTORY

# current status of node
def get_status(model, node):
    return model.status[node]

# Get Node Degree
def get_degree(model, node):
    return model.graph.graph.degree(node)

# average degree of the neighbours of a node
def get_avg_neighbour_degree(model, node):
    return nx.average_neighbor_degree(model.graph.graph)[node]

# is the current node a traveller
def is_traveler(travelers, node):
    return node in travelers

# get number of neighbors of a certain status
def get_num_neighbour_status(model, node, target_status=0):
    status_count = 0
    for neighbour in model.graph.neighbors(node):
        if model.status[neighbour] == target_status:
            status_count += 1
    return status_count


