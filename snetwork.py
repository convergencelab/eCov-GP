'''
Author:     James Hughes
Date:       June 9, 2020

Version:    0.6


Change Log:
    0.1 (June 9, 2020): 
        - Initial version.

    0.2 (June 25, 2020):
        - Watts-Strogatz Graph added as a type of random network
        - I am not that confident in it though as the way it is implemented seems to enforce a fixed edge number. In other words, there is no variation in the number of neighbours that we would see in reality 

    0.3 (July 8, 2020):
        - Switched to 'connected' WS graph (to make sure we end up with a connected graph). Although unlikely to be disconnected, this is _safer_

    0.4 (July 8, 2020):
        - Switched to newman watts stogatz as it has a probability of adding NEW edges (so we get a better range of connectivity)

    0.5 (July 16, 2020):
        - Added the ability to use Barabasi-Albert graph
        - Done because it seems to popular 
        - http://www-math.mit.edu/~apost/courses/18.204_2018/Lee_Bernick_paper.pdf

    0.6 (November 10, 2020):
        - Added Powerlaw Cluster Graph
            - https://networkx.org/documentation/stable/reference/generated/networkx.generators.random_graphs.powerlaw_cluster_graph.html#networkx.generators.random_graphs.powerlaw_cluster_graph
        - Kinda' like a BA graph, but makes it cluster
        - This idea came from the talk at Dalhousie where it was suggested by to have better clustering graphs


End Change Log

setup the network

New function to just return the model. 

'''

###########
# Imports #
###########
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import networkx as nx
import networkx.algorithms.community as comm
import os
import random

from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence



##################
# Epidemic Setup #
##################

def setup_network(alpha, beta, gamma, infected, directory=None, name=None, size=None, edge_p=None, knn=None, rewire_p=None, drop=None, m=None, n_edges=None, triangle_p=None):

    # Network topology
    
    # Create Graph  
    if edge_p != None:
        print("Making ER Graph")
        g = nx.erdos_renyi_graph(size, edge_p)

    elif knn != None:
        print("Making NWS Graph with drops")
        g = nx.newman_watts_strogatz_graph(size, knn, rewire_p)

        # drop random edges
        for i in range(drop):
            e = random.choice(list(g.edges))
            g.remove_edge(e[0], e[1])

    elif m != None:
        print("Making BA Graph")
        g = nx.barabasi_albert_graph(size, m)

    elif triangle_p != None:
        print("Making Powerlaw Cluster Graph")
        g = nx.powerlaw_cluster_graph(n=size, m=n_edges, p=triangle_p)

    else:    
        print("Loading custom Graph")
        g = nx.read_adjlist(os.path.join(directory, name), delimiter='\t', nodetype=int)

    # Model selection
    m = ep.SEIRModel(g)

    # Model Configuration
    cfg = mc.Configuration()
    cfg.add_model_parameter('beta', beta)
    cfg.add_model_parameter('gamma', gamma)
    cfg.add_model_parameter('alpha', alpha)
    cfg.add_model_parameter("fraction_infected", infected)
    m.set_initial_status(cfg)

    return m

