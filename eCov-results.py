'''
Author:     James Hughes
Date:       May 22, 2020

Version:    0.1

Change Log:
    0.1: 
        - Initial version.
        - Built from code from eCov-GP. 


End Change Log

'''

###########
# Imports #
###########

import math
import matplotlib.pyplot as plt
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import networkx as nx
import networkx.algorithms.community as comm
import numpy as np
import operator
import os
import pickle

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence

from networkx.drawing.nx_agraph import graphviz_layout


###########
# PARAMS  #
###########

RESULTS_DIRECTORY = "./output/"
RESULTS_NAME = "05-22-2020_20-01-18.pkl"


###############
# DEAP Setup  #
###############

# Language 

def if_then_else(in1, out1, out2):
    return out1 if in1 else out2

def protectedDiv(a, b):
    try:
        q = a / b
    except ZeroDivisionError:
        q = 1
        
    return q

language = gp.PrimitiveSetTyped("MAIN", 
                                [#float,       # Node Status (0 - susceptible, 1 - exposed, 2 - infected, 3 - removed)
                                 float,       # Degree of Node
                                 #float,      # Average degree of node neighbours
                                 #float,       # Number of neighbours susceptible + exposed
                                 float,       # Number of neighbours infected
                                 #float,       # Number of neighbours removed
                                 bool,      # Is traveler
                                 float,       # Number of mitigations available
                                 #bool,      # Is mitigation available
                                 #float,       # Total number of susceptible and exposed
                                 float,       # Total number of infected
                                 #float,       # Total number of removed
                                 #float,     # Average distance between all susceptible and exposed
                                 #float,     # Average distance between all infected
                                 #float,     # Average distance between all removed 
                                 #float,     # Iteration number
                                ],
                                bool,       # Do we vaccinate?
                                "ARG")

#language.renameArguments(ARG0='STATUS')
language.renameArguments(ARG0='DEGREE')
#language.renameArguments(ARG1='NB_DEGREE')
#language.renameArguments(ARG2='NB_SUSEXP')
language.renameArguments(ARG1='NB_INFECT')
#language.renameArguments(ARG4='NB_REMOVE')
language.renameArguments(ARG2='TRAVELER')
language.renameArguments(ARG3='NUM_MITIGAT')
#language.renameArguments(ARG7='MITIGATE')
#language.renameArguments(ARG8='NUM_SUSEXP')
language.renameArguments(ARG4='NUM_INFECT')
#language.renameArguments(ARG10='NUM_REMOVE')
#language.renameArguments(ARG12='AVG_SUSEXP')
#language.renameArguments(ARG13='AVG_INFECT')
#language.renameArguments(ARG14='AVG_REMOVE')
#language.renameArguments(ARG15='ITERATION')

# Arithmatic 
language.addPrimitive(operator.add, [float, float], float)
language.addPrimitive(operator.sub, [float, float], float)
#language.addPrimitive(operator.mul, [float, float], float)
#language.addPrimitive(protectedDiv, [float, float], float)

# Boolean
language.addPrimitive(operator.and_, [bool, bool], bool)
language.addPrimitive(operator.or_, [bool, bool], bool)
language.addPrimitive(operator.not_, [bool], bool)

# Math & Logic
language.addPrimitive(operator.eq, [float, float], bool)
#language.addPrimitive(operator.ne, [float, float], bool)
language.addPrimitive(operator.lt, [float, float], bool)
#language.addPrimitive(operator.le, [float, float], bool)
language.addPrimitive(operator.gt, [float, float], bool)
#language.addPrimitive(operator.ge, [float, float], bool)
language.addPrimitive(if_then_else, [bool, bool, bool], bool)

# Constants
#language.addEphemeralConstant("rand_float", lambda: random.random()*100, float)
#language.addEphemeralConstant("rand100", lambda: random.random() * 100, float)
#language.addEphemeralConstant("rand_bool", lambda: True if random.random() < 0.5 else False, bool)
language.addEphemeralConstant("rand_int", lambda: random.randint(0,15), float)
language.addTerminal(False, bool)
language.addTerminal(True, bool)

toolbox = base.Toolbox()

creator.create("FitnessMin", base.Fitness, weights=(1,-1))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox.register("expr", gp.genHalfAndHalf, pset=language, min_=1, max_=4)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=language)

# Operators
#toolbox.register("evaluate", evaluate_individual)
toolbox.register("elitism", tools.selBest, k=1)
toolbox.register("select", tools.selTournament, tournsize=2)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=language)

## Bloat rules 
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=5))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=5))

toolbox.decorate("mate", gp.staticLimit(key=len, max_value=32))
toolbox.decorate("mutate", gp.staticLimit(key=len, max_value=32))

# Statistics Bookkeeeping
stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
stats_size = tools.Statistics(len)
mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
mstats.register("avg", np.mean)
mstats.register("std", np.std)
mstats.register("min", np.min)
mstats.register("max", np.max)

logbook = tools.Logbook()

#############
# File I/O  #
#############

results = pickle.load(open(os.path.join(RESULTS_DIRECTORY, RESULTS_NAME), 'rb'))

population = results["population"]
logbook = results["logbook"]


###############################
# Visualize Results as Trees  #
###############################

def draw_tree(ind):
    nodes, edges, labels = gp.graph(ind)

    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    pos = graphviz_layout(g, prog="dot")

    nx.draw_networkx_nodes(g, pos)
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_labels(g, pos, labels)
    plt.show()

os.environ['PATH'] = os.environ['PATH']+';'+os.environ['CONDA_PREFIX']+r"\Library\bin\graphviz"

draw_tree(population[0])



########################
# Run on SEIR network  #
########################

# TODO
