'''
Author:     James Hughes
Date:       July 8, 2020

Version:    0.3


Change Log:
    0.1 (July 8, 2020): 
        - Initial version.

    0.2 (July 22, 2020):
        - Updated alpha to reflect the latent period, NOT a probability
   
    0.3 (September 1, 2020):
        - Changed param values to get better graph stats (avg. degree, avg. dist)

End Change Log

Testing parameters to see how well a simulation works with given settings. 

'''
import matplotlib.pyplot as plt
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import networkx as nx
import numpy as np
import os
import random


from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence

from networkx.drawing.nx_agraph import graphviz_layout

from measures import * 
from language import *

import evaluate
import sgp
import snetwork

# Graph & Disease
GRAPH_DIRECTORY = './../GRAPHS/sg_infectious_graphs/'
GRAPH_NAME = 'nonweightededges_2009_05_03.dat'

BETA = 0.09            # Spread Probability (25% works for Wendy graph)
GAMMA = 0.133           # Removal Probability. Based on 7 day, from sources
ALPHA = 6.4             # Latent period. Based on 6.4 days, from sources
INFECTED_0 = 0.02
ITERATIONS = 98  
GRAPH_SIZE = 500

# For ER graph
EDGE_p = 0.017

# For NWS graph
KNN = 10
REWIRE_p = 0.20
DROP = 1000

# for BA graph
M = 3      

      
# Get the average degree of the graph
def get_average_degree(model):
    d = []

    for n in range(len(model.graph.graph.nodes)):
        d.append(model.graph.graph.degree(n))

    return np.average(d), np.min(d), np.max(d)

# Get the average distance between nodes
def get_average_dist(model):
    # add all the distances to this list
    # in the end we will average these values    
    distances = []

    nodes = list(model.graph.graph.nodes)

    # Only calc the top right triangle of distances
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            distances.append(nx.shortest_path_length(model.graph.graph, nodes[i], nodes[j]))

    # If there are no distances to take an average of
    if len(distances) < 1:
        avg_min_max = 0,0,0
    else:
        avg_min_max = (np.average(distances), np.min(distances), np.max(distances))

    # return the average
    return avg_min_max


os.environ['PATH'] = os.environ['PATH']+';'+os.environ['CONDA_PREFIX']+r"\Library\bin\graphviz"

#model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
# ER
#model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, edge_p=EDGE_p, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
# NWS
#model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, rewire_p=REWIRE_p, knn=KNN, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
# BA
model = snetwork.setup_network(size=GRAPH_SIZE, m=M, alpha=ALPHA, beta=BETA, gamma=GAMMA, infected=INFECTED_0)

print(len(model.graph.graph.nodes))
print(len(model.graph.graph.edges))

avg_degree = get_average_degree(model)
print(avg_degree)
dist = get_average_dist(model)
print(dist)

'''
# List to record network changes throughout simulation
iterations = []

# Test simulation
for i in range(ITERATIONS):
    iterations.append(model.iteration())

# See curves
trends = model.build_trends(iterations)
viz = DiffusionTrend(model, trends)
#viz.plot()

'''
#nx.draw(model.graph.graph,node_size=25, alpha=0.75, width=0.5, edge_color='grey')         
#plt.show()
'''
mvc = get_min_vertex_cover(model)
print(len(mvc))
'''
