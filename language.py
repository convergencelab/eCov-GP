'''
Author:     James Hughes
Date:       June 8, 2020

Version:    0.2


Change Log:
    0.1 (June 8, 2020): 
        - Initial version.

    0.2 (June 17, 2020):
        - Updated to incorporate new measure of average degree


End Change Log

Application of Mitigation functions are included (both single node and ring).

All the functions for the language are within. GP language is completly defined within this script. 

Perhaps in a future version we have a function in here that gets called and returns the code


'''

###########
# Imports #
###########

import math
import numpy as np
import operator
import random

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp


###########################
# Mitigation Applications #
###########################

# Apply single Mitigation
# return the number of nodes mitigated
def mitigate_self(model, node):
    model.status[node] = 3
    return 1

# 'Ring Mitigation'
# Apply mitigation to neighbours
# This one will likely matter only for infected nodes
# Since the number of neighbours may exceed the number
# of available mitigations, we will:
# (a) Shuffle, so we randomly apply them to the neighbours
# (b) Only apply mitigation for the amount we have
# return the number of nodes mitigated
def mitigate_neighbours(model, node, mitigation_available):

    # Get the nodes neighbours
    neighbours = random.sample(model.graph.neighbors(node), mitigation_available)

    mitigation_count = 0    

    for n in neighbours:

        # Only need to mitigate those that can be
        # NOTE: future versions may want to apply mitigation to infected
        #       as we don't REALLY know that infected are infected
        #       this would waste mitigations, but more realistic 
        if model.status[n] == 0:
            model.status[n] = 3
            mitigation_count += 1

    return mitigation_count

############
# Language #
############
def if_then_else(in1, out1, out2):
    return out1 if in1 else out2


def protectedDiv(a, b):
    try:
        q = a / b
    except ZeroDivisionError:
        q = 1
        
    return q

# Inputs labeled below
language = gp.PrimitiveSetTyped("MAIN", 
                                [#float,       # Node Status (0 - susceptible, 2 - exposed, 1 - infected, 3 - removed)
                                 float,       # Degree of Node
                                 float,      # Average degree of node neighbours
                                 float,       # Number of neighbours susceptible + exposed
                                 float,       # Number of neighbours infected
                                 #float,       # Number of neighbours removed
                                 bool,      # Is traveler
                                 bool,      # In Minimal Vertex Cover
                                 float,     # Average degree of Nodes in Graph
                                 float,     # Average shortest distance between nodes in Graph
                                 float,     # Average Shortest dist from single node to all others
                                 #float,       # Number of mitigations available
                                 #bool,      # Is mitigation available
                                 float,       # Total number of susceptible and exposed
                                 float,       # Total number of infected
                                 float,       # Total number of removed
                                 float,         # Number of times a vertex is in a shortest path
                                 #float,     # Shortest distance from susexp node to an infected node
                                 #float,     # Average distance between all susceptible and exposed
                                 #float,     # Average distance between all infected
                                 #float,     # Average distance between all removed 
                                 float,      # Minimal Vertex Cover 
                                 float,      # Clustering Coef
                                 #float,     # Iteration number
                                ],
                                bool,       # Do we vaccinate?
                                "ARG")

#language.renameArguments(ARG0='STATUS')
language.renameArguments(ARG0='DEGREE')
language.renameArguments(ARG1='NB_DEGREE')
language.renameArguments(ARG2='NB_SUSEXP')
language.renameArguments(ARG3='NB_INFECT')
#language.renameArguments(ARG4='NB_REMOVE')
language.renameArguments(ARG4='TRAVELER')
language.renameArguments(ARG5='MVC')
language.renameArguments(ARG6='AVG_DEGREE')
language.renameArguments(ARG7='AVG_DIST_ALL')
language.renameArguments(ARG8='AVG_DIST_SGL')
#language.renameArguments(ARG7='NUM_MITIGAT')
#language.renameArguments(ARG7='MITIGATE')
language.renameArguments(ARG9='NUM_SUSEXP')
language.renameArguments(ARG10='NUM_INFECT')
language.renameArguments(ARG11='NUM_REMOVE')
language.renameArguments(ARG12='NUM_SHORT')
#language.renameArguments(ARG11='SHORT_DIST')
#language.renameArguments(ARG12='AVG_SUSEXP')
#language.renameArguments(ARG13='AVG_INFECT')
#language.renameArguments(ARG14='AVG_REMOVE')
language.renameArguments(ARG13='PR')
language.renameArguments(ARG14='CCOEF')
#language.renameArguments(ARG12='ITERATION')


# Arithmatic 
language.addPrimitive(operator.add, [float, float], float)
language.addPrimitive(operator.sub, [float, float], float)
language.addPrimitive(operator.mul, [float, float], float)
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
language.addEphemeralConstant("rand_float_0-100", lambda: random.random()*1000, float)
#language.addEphemeralConstant("rand100", lambda: random.random() * 100, float)
#language.addEphemeralConstant("rand_bool", lambda: True if random.random() < 0.5 else False, bool)
language.addEphemeralConstant("rand_int_0-33", lambda: random.randint(0,33), float)
language.addTerminal(False, bool)
language.addTerminal(True, bool)

