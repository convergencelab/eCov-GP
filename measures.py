'''
Author:     James Hughes
Date:       June 8, 2020

Version:    0.8


Change Log:
    0.1 (June 8, 2020): 
        - Initial version

    0.2 (June 17, 2020):
        - Add average degree static graph measure
    
    0.3 (July 8, 2020):
        - Add minimal vertex cover approx to the list of static measures 
        - Add local measure to tell is a given vertex is in the minimal vertex cover
        - This was Athar's idea (good one too)
        - I DO NOT THINK IT WORKS RIGHT THOUGH AS IMPLEMENTED

    0.4 (August 10, 2020):
        - Changes average degree of node to only calculate the avg. degree on a single node, not all (way faster) 

    0.5 (August 17, 2020):
        - Added 
            - get_shortest_distances_all_nodes
            - get_shortest_distance
        - Now we have a way to know how FAR away nodes of a certain type are

    0.6 (September 1, 2020):
        - Added average distance to all nodes

    0.7 (September 30, 2020):
        - Catch key error exception on shortest dist in case graph happens to not be connected. 
            - If this happens, just ignore that path

    0.8 (October 15, 2020:
        - Added measures:
            * Average shortest dist from one node to all other nodes
            * Number of times a node exists in a path from all nodes to all nodes
            * Pagerank 

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
import networkx.algorithms.approximation as appr
import numpy as np
import random

from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence

###########################
# Graph Measure Functions #
###########################

###################
# STATIC MEASURES #
###################

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

# Approx minimal vertex cover
# WARNING: 
#       - Most of these graphs have almost all edges in this
def get_min_vertex_cover(model):
    return appr.min_weighted_vertex_cover(model.graph)

# Get the average degree of the graph
def get_average_degree(model):
    d = []

    for n in range(len(model.graph.graph.nodes)):
        d.append(model.graph.graph.degree(n))

    return np.average(d)

# Find shortest distance from all nodes to every other node
def get_shortest_distances_all_nodes(model):
    return dict(nx.shortest_path_length(model.graph.graph))

# Find average distance from all nodes to every other node
def get_avg_distances_all_nodes(model):
     # add all the distances to this list
    # in the end we will average these values    
    distances = []

    nodes = list(model.graph.graph.nodes)

    # Only calc the top right triangle of distances since symetric 
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            try:
                distances.append(nx.shortest_path_length(model.graph.graph, nodes[i], nodes[j]))
            except nx.NetworkXNoPath:
                distances.append(9999999)

    # If there are no distances to take an average of
    if len(distances) < 1:
        avg = 0
    else:
        avg = np.average(distances)

    # return the average
    return avg


# Return a list of each node's average shortest
# path length to all other nodes in the graph
def get_node_avg_distances_all_nodes(model):
    average_path_lengths = []
    paths = dict(nx.shortest_path_length(model.graph.graph))
    nodes = list(model.graph.graph.nodes)

    for i in range(len(nodes)):
                
        node_lengths = []
        for j in range(0, len(nodes)):
            try:
                node_lengths.append(paths[nodes[i]][nodes[j]])
            except nx.NetworkXNoPath:
                distances.append(9999999)
        average_path_lengths.append(np.average(node_lengths))

    return average_path_lengths



# Find shortest path from all nodes to every other node
def get_shortest_paths_all_nodes(model):
    return dict(nx.shortest_path(model.graph.graph))


# Number of times each node exists in the 
# shortest path between any two nodes
# This does count itself in paths to/from itself
# For example, 0 is in the shortest path from 0 to X
# WARNING, I THINK THIS ONLY CONSIDERS ONE PATH IF MORE THAN 
#  ONE SHORTEST PATH EXISTS!!!!!!!
def get_node_number_shortest_paths(model):
    paths = dict(nx.shortest_path(model.graph.graph))
    nodes = list(model.graph.graph.nodes)

    counts = np.zeros(len(nodes))

    # For each node pair (each)
    for i in range(nodes):
        for j in range(nodes):
            
            # Iterate over the shortest path
            # and add the indicies to the counts array
            for k in len(paths[i][j]):
                counts[paths[i][j][k]] += 1

    return counts
    
# Gets the pagerank
# Not sure how helpful this will really be
def get_page_rank(model):
    return nx.algorithms.link_analysis.pagerank_alg.pagerank(model.graph.graph)



########################
# WHOLE GRAPH MEASURES #
########################

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
def get_avg_dist_between_nodes(dists, nodes, proportion=1.0):

    # Get a random subset of the nodes baseed on the
    # proportion of nodeswe will consider in our sample
    nodes = random.sample(nodes, int(len(nodes)*proportion))

    # add all the distances to this list
    # in the end we will average these values    
    distances = []

    # Only calc the top right triangle of distances
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            distances.append(dists[nodes[i]][nodes[j]])

    # If there are no distances to take an average of
    if len(distances) < 1:
        avg = 0
    else:
        avg = np.average(distances)

    # return the average
    return avg

########################
# SINGLE GRAPH MEASURE #
########################

# current status of node
def get_status(model, node):
    return model.status[node]

# Get Node Degree
def get_degree(model, node):
    return model.graph.graph.degree(node)

# average degree of the neighbours of a node
def get_avg_neighbour_degree(model, node):
    #return nx.average_neighbor_degree(model.graph.graph)[node]
    return nx.average_neighbor_degree(model.graph.graph, nodes=[node])[node]

# is the current node a traveller
def is_traveler(travelers, node):
    return node in travelers

# Is the current node in the minimal vertex cover
def is_in_min_cover(mvc, node):
    return node in mvc

# get number of neighbors of a certain status
def get_num_neighbour_status(model, node, target_status=0):
    status_count = 0
    for neighbour in model.graph.neighbors(node):
        if model.status[neighbour] == target_status:
            status_count += 1
    return status_count

# Finds the shortest distance from node to a node of a certain type (targets)
def get_shortest_distance(dists, node, targets):
    shortest = 9999999    # should do better here
    for t in targets:
        try:
            if dists[node][t] < shortest:
                shortest = dists[node][t]
        except KeyError:
                pass        # just do nothing
    return shortest


