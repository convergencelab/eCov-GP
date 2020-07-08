'''
Author:     James Hughes
Date:       June 9, 2020

Version:    0.3


Change Log:
    0.1 (June 9, 2020): 
        - Initial version.

    0.2 (June 25, 2020):
        - Watts-Strogatz Graph added as a type of random network
        - I am not that confident in it though as the way it is implemented seems to enforce a fixed edge number. In other words, there is no variation in the number of neighbours that we would see in reality 

    0.3 (July 8, 2020):
        - Switched to 'connected' WS graph (to make sure we end up with a connected graph). Although unlikely to be disconnected, this is _safer_


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

from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence



##################
# Epidemic Setup #
##################

def setup_network(alpha, beta, gamma, infected, directory=None, name=None, size=None, edge_p=None, knn=None, rewire_p=None):

    # Network topology
    
    # Create Graph  
    if directory == None:
        g = nx.erdos_renyi_graph(size, edge_p)
    elif edge_p == None:
        g = nx.connected_watts_strogatz_graph(size, knn, rewire_p)
    else:    
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

