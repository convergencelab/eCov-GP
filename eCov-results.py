'''
Author:     James Hughes
Date:       May 22, 2020

Version:    0.4

Change Log:
    0.1: 
        - Initial version.
        - Built from code from eCov-GP. 

    0.2:
        - New function to execute individual population members on an SEIR model. 

    0.3 (May 28, 2020):
        - Update to the evaluate_individual function to return lists of dictionaries for node changes and mitigation changes
        - Mitigation trends function
        - Functions to convert trends and iterations to simple summary numbers (more useful for GP itself)

    0.4 (May 30, 2020):
        - Add a boolean flag to allow unused mitigations to be used at next evaluation period


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
import random

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
SUB_DIRECTORY = ""
RESULTS_NAME = "05-29-2020_23-52-11.pkl"

# Graph & Disease
GRAPH_DIRECTORY = './../../GRAPHS/'
GRAPH_NAME = 'github_notop.dat'
BETA = 0.025            # Spread Probability
GAMMA = 0.133           # Incubation Probability. Based on 7 day, from sources
ALPHA = 0.175           # Recovery Probability. Based on 5.2 days, from sources
INFECTED_0 = 0.01
GRAPH_SIZE = 500
EDGE_p = 0.04
ITERATIONS = 140        
MEASURE_EVERY = 7
MITIGATIONS_PER_MEASURE = 30
ROLLOVER = True

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


######################
# Fitness Evaluation #
######################
   
# Fitness Function
def evaluate_individual(chromosome):
    f = toolbox.compile(expr=chromosome)

    max_infected = 0
    total_infected = 0
    total_mitigation = 0
    total_mitigation_effective = 0
    rollover_mitigations = 0
    

    # List to record network changes throughout simulation
    iterations = []
    
    # List to record network changes about mitigation strategies 
    iterations_mitigations = []

    for i in range(ITERATIONS):

        # If it is a day we evaluate our network and apply mitigation
        if i != 0 and i % MEASURE_EVERY == 0:
            # Identify those that are able to hav emitigation applied
            # Remember, we pretend we do not know that exposed are exposed
            susceptible = get_all_of_status(model)
            exposed = get_all_of_status(model, target_status=1)
            #infected = get_all_of_status(model, target_status=2)
            susexp = susceptible + exposed
            # Shuffle because we have limited resources and don't want any ordering
            random.shuffle(susexp)          

            
            num_suscept = get_num_nodes(model)
            num_exposed = get_num_nodes(model, target_status=1)
            num_susexp = num_suscept + num_exposed
            num_infected = get_num_nodes(model, target_status=2)
            num_removed = get_num_nodes(model, target_status=3)

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
                
                if mitigations_available(MITIGATIONS_PER_MEASURE + rollover_mitigations, mitigations_used):
                    node_status = get_status(model, s)
                    node_degree = get_degree(model, s)
                    avg_neighbour_degree = get_avg_neighbour_degree(model, s)
                    neighbour_susexp = get_num_neighbour_status(model, s, target_status=0) + get_num_neighbour_status(model, s, target_status=1)
                    neighbour_infected = get_num_neighbour_status(model, s, target_status=2) 
                    neighbour_removed = get_num_neighbour_status(model, s, target_status=3) 
                    traveler = is_traveler(travelers, s)
                    num_mitigation = mitigations_available(MITIGATIONS_PER_MEASURE + rollover_mitigations, mitigations_used)
                    mitigation = get_cur_mitigations(MITIGATIONS_PER_MEASURE + rollover_mitigations, mitigations_used)

                    do_we_mitigate = f(
                                        node_degree,
                                        #avg_neighbour_degree,
                                        #neighbour_susexp, 
                                        neighbour_infected,
                                        #neighbour_removed,
                                        traveler,
                                        num_mitigation,
                                        #mitigation,
                                        #num_susexp,
                                        num_infected,
                                        #num_removed,
                                        #i,
                                        )
                    if do_we_mitigate:
                        if node_status == 0:
                            cur_num_mitigated = mitigate_self(model, s)
                            mitigations_used += cur_num_mitigated
                            mitigations_used_effective += cur_num_mitigated
                            mitigations_step['status'][s] = 4

                        # Apply mitigation to exposed, but this wastes mitigation                        
                        else:
                            mitigations_used += 1
                       
                else:
                    break

            # If we are rolloigover
            if ROLLOVER:
                # rollovers can accumulate over multiple periods
                rollover_mitigations = (MITIGATIONS_PER_MEASURE + rollover_mitigations) - mitigations_used

            total_mitigation += mitigations_used
            total_mitigation_effective += mitigations_used_effective

            mitigations_step['node_count'][4] = total_mitigation_effective
            mitigations_step['status_delta'][4] = mitigations_used_effective
            mitigations_step['total_mitigations']['total'] = mitigations_used
            mitigations_step['total_mitigations']['effective'] = mitigations_used_effective
            mitigations_step['total_mitigations']['ineffective'] = mitigations_used - mitigations_used_effective

            iterations_mitigations.append(mitigations_step)

        current_infected = get_num_nodes(model, target_status=2)
        total_infected += current_infected
        max_infected = max(max_infected, current_infected)

        iterations.append(model.iteration())
        

    final_num_susceptible = get_num_nodes(model)    
    final_num_removed = get_num_nodes(model, target_status=3)

    # Use this between chromosome evals
    # Will reset network with same params
    # BUT, the same nodes will NOT start infected
    # Would this make more sense in evaluate_population?
    model.reset()

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



def convert_iterations(iterations):
    trends = model.build_trends(iterations)
    final_susceptible = iterations[-1]['node_count'][0]
    final_removed = iterations[-1]['node_count'][3]
    max_infected = max(trends[0]['trends']['node_count'][2])
    total_infected = sum(trends[0]['trends']['node_count'][2])  # Area under curve 
    return final_susceptible, max_infected, total_infected, final_removed, 

def convert_iterations_mitigations(iterations_mitigations):
    trends = mitigation_trends(iterations_mitigations)
    total = trends[0]['trends']['node_count']['total'][-1]
    effective = trends[0]['trends']['node_count']['effective'][-1]
    ineffective = trends[0]['trends']['node_count']['ineffective'][-1]
    
    return total, effective, ineffective, 


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

results = pickle.load(open(os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, RESULTS_NAME), 'rb'))

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


for i in range(len(population)): 
    print(i, population[i].fitness)
    #draw_tree(population[i])

##################
# Epidemic Setup #
##################

# Network topology
#g = nx.erdos_renyi_graph(4000, 0.005)
g = nx.erdos_renyi_graph(GRAPH_SIZE, EDGE_p)
#g = nx.read_adjlist(os.path.join(GRAPH_DIRECTORY, GRAPH_NAME), delimiter='\t', nodetype=int)


# Model selection
model = ep.SEIRModel(g)

# Model Configuration
cfg = mc.Configuration()
cfg.add_model_parameter('beta', BETA)
cfg.add_model_parameter('gamma', GAMMA)
cfg.add_model_parameter('alpha', ALPHA)
cfg.add_model_parameter("fraction_infected", INFECTED_0)
model.set_initial_status(cfg)

# Identify travelers
travelers = get_travelers(model)

########################
# Run on SEIR network  #
########################

def diffusion_trend(ind):
    iterations, iterations_mitigations = evaluate_individual(ind)
    trends = model.build_trends(iterations)
    # Visualization
    viz = DiffusionTrend(model, trends)
    viz.plot()
    viz = DiffusionPrevalence(model, trends)
    viz.plot()
    return iterations, trends


#diffusion_trend(population[0])

