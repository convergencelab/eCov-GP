'''
Author:     James Hughes
Date:       July 8, 2020

Version:    0.2


Change Log:
    0.1 (July 8, 2020): 
        - Initial version.

    0.2 (July 22, 2020):
        - Updated alpha to reflect the latent period, NOT a probability
   
        

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
GRAPH_DIRECTORY = './../GRAPHS/Guelph/'
GRAPH_NAME = 'Graph0_notop.dat'

BETA = 0.05             # Spread Probability (25% works for Wendy graph)
GAMMA = 0.133           # Incubation Probability. Based on 7 day, from sources
ALPHA = 6.4             # Latent period. Based on 6.4 days, from sources
INFECTED_0 = 0.01
ITERATIONS = 91  

# For ER graph
GRAPH_SIZE = 500
EDGE_p = 0.04

# For NWS graph
KNN = 20
REWIRE_p = 0.20
DROP = 1000

# for BA graph
M = 9      

      
# Get the average degree of the graph
def get_average_degree(model):
    d = []

    for n in range(len(model.graph.graph.nodes)):
        d.append(model.graph.graph.degree(n))

    return np.average(d), np.min(d), np.max(d)


os.environ['PATH'] = os.environ['PATH']+';'+os.environ['CONDA_PREFIX']+r"\Library\bin\graphviz"

#model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
# ER
#model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, edge_p=EDGE_p, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
# NWS
model = snetwork.setup_network(directory=GRAPH_DIRECTORY, name=GRAPH_NAME, size=GRAPH_SIZE, rewire_p=REWIRE_p, knn=KNN, alpha=ALPHA, drop=DROP, beta=BETA, gamma=GAMMA, infected=INFECTED_0)
# BA
#model = snetwork.setup_network(size=GRAPH_SIZE, m=M, alpha=ALPHA, beta=BETA, gamma=GAMMA, infected=INFECTED_0)

print(get_average_degree(model))

# List to record network changes throughout simulation
iterations = []

# Test simulation
for i in range(ITERATIONS):
    iterations.append(model.iteration())

# See curves
trends = model.build_trends(iterations)
viz = DiffusionTrend(model, trends)
viz.plot()


nx.draw(model.graph.graph,node_size=25, alpha=0.75, width=0.5, edge_color='grey')         
plt.show()

mvc = get_min_vertex_cover(model)
#print(len(mvc))

