'''
Author:     James Hughes
Date:       May 19, 2020

Version:    0.1

Change Log:
    0.1: 
        - Initial version.
    
    0.2:
        - Remove the end visualization.
        - Save final results to pickled file.
        - Visualization and results interpretation will occur in separate script. 

End Change Log



A GP search for effective vaccination strategies for a given graph

This version is relatively simple:
- Will be single objective. 
    - Will probably eventually want to make multi
        - Min tree size
        - Min max infected
        - Integral under infected curve
        - Total infected over period
        - Min mitigation used
- SEIR model (no E', where E' is exposed AND infected, but not detected)
- No fancy node info (age, pre existing conditions, etc.)
- Simple graph statistics 
    - Static
        - Travelers (CURRENT VERSION HAS A VERY HACK-IE IMPLEMENTATION)
    - Whole Graph
        - Number of certain status
        - Number of mitigations used
        - Is mitigation available? (boolean)
        - ***** (REMOVED FOR THIS VERSION DUE TO TIME CONSTRAINTS) Average distance between nodes of a given status
    - Single/Local Measures
        - Current Status
        - Node Degree
        - Average degree of neighbours
        - is traveler? (boolean)
        - Get number of neighbours of certain status

- Atomic Heuristics
    - For Susceptible & Exposed
        - Mitigate Self
    - For Infected
        - Mitigate Neighbours (ring vaccination)
    - MIGHT only work on susceptible/exposed (no looking at ring vaccination yet) 

I think to start the trees will simply be a boolean expression. If true, vac, otherwise, no. 

'''

###########
# Imports #
###########
import csv
import datetime
import itertools
import math
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

###########
# PARAMS  #
###########

# GP System
DATA_DIRECTORY = "./"
RESULTS_DIRECTORY = "./output/"
DATA_NAME = ""
POPULATION = 50
GENERATIONS = 50
CROSSOVER = 0.75
MUTATION = 0.1

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
MITIGATIONS_PER_MEASURE = 20
###########


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

'''
language.renameArguments(
                        #ARG0='STATUS',
                         ARG0='DEGREE',
                         #ARG2='NB_DEGREE',
                         ARG1='NB_SUSEXP',
                         ARG2='NB_INFECT',
                         ARG3='NB_REMOVE',
                         ARG4='TRAVELER',
                         ARG5='#MITIGAT',
                         ARG6='MITIGATE',
                         ARG7='#SUSEXP',
                         ARG8='#INFECT',
                         ARG9='#REMOVE',
                         #ARG12='AVG_SUSEXP',
                         #ARG13='AVG_INFECT',
                         #ARG14='AVG_REMOVE',
                        )
'''


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


######################
# Fitness Evaluation #
######################
   
# Fitness Function
def evaluate_individual(chromosome):
    f = toolbox.compile(expr=chromosome)

    max_infected = 0
    total_infected = 0
    total_mitigation = 0

    for i in range(ITERATIONS):

        # If it is a day we evaluate our network and apply mitigation
        if i % MEASURE_EVERY == 0:
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

            mitigations_used = 0

            # Evaluate nodes
            # Only consider susceptible and exposed currently
            # In future, we could consider infected and do neighbour/ring mitigation
            for s in susexp:
                
                if mitigations_available(MITIGATIONS_PER_MEASURE, mitigations_used):
                    node_status = get_status(model, s)
                    node_degree = get_degree(model, s)
                    avg_neighbour_degree = get_avg_neighbour_degree(model, s)
                    neighbour_susexp = get_num_neighbour_status(model, s, target_status=0) + get_num_neighbour_status(model, s, target_status=1)
                    neighbour_infected = get_num_neighbour_status(model, s, target_status=2) 
                    neighbour_removed = get_num_neighbour_status(model, s, target_status=3) 
                    traveler = is_traveler(travelers, s)
                    num_mitigation = mitigations_available(MITIGATIONS_PER_MEASURE, mitigations_used)
                    mitigation = get_cur_mitigations(MITIGATIONS_PER_MEASURE, mitigations_used)

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
                            mitigations_used += mitigate_self(model, s)

                        # Apply mitigation to exposed, but this wastes mitigation                        
                        else:
                            mitigations_used += 1
                       
                else:
                    break

            total_mitigation += mitigations_used

        

        current_infected = get_num_nodes(model, target_status=2)
        total_infected += current_infected
        max_infected = max(max_infected, current_infected)

        model.iteration()

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
    return final_num_susceptible, total_mitigation

def evaluate_population(pop):
    # Only worry about individuals with INVALID fitness values
    # This will save some time
    #invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    #fitnesses = list(map(toolbox.evaluate, invalid_ind))
    fitnesses = list(map(toolbox.evaluate, pop))
    #for ind, fit in zip(invalid_ind, fitnesses):
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit    


#################################################
# Set up chromosomes, population, and operators #
#################################################
toolbox = base.Toolbox()

# Magic code to make it parallel?
# Must be run like this though:
#   ipython -m scoop eCov-GP.py
from scoop import futures
toolbox.register("map", futures.map)


creator.create("FitnessMin", base.Fitness, weights=(1,-1))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox.register("expr", gp.genHalfAndHalf, pset=language, min_=1, max_=4)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=language)

# Operators
toolbox.register("evaluate", evaluate_individual)
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



#######################
# Evolutionary Search #
#######################

population = toolbox.population(n=POPULATION)

print('Starting Evolution')
for g in range(GENERATIONS):

    if g % (0.1 * GENERATIONS) == 0:
        print(g/GENERATIONS)

    evaluate_population(population)
    record = mstats.compile(population)
    logbook.record(gen=g, **record)
    
    # Elitism
    #best = toolbox.elitism(population)
    #best_clone = toolbox.clone(best)
    
    # Selection
    #offspring = toolbox.select(population, len(population)-1)
    offspring = toolbox.select(population, len(population))
    offspring_clone = list(map(toolbox.clone, offspring))
        
    # Simplified genetic operators 
    new_population = algorithms.varAnd(offspring_clone, toolbox, CROSSOVER, MUTATION)

    # replace the population with the new population
    #population[:] = best_clone + new_population
    population[:] = new_population

    
print('Ending Evolution')

evaluate_population(population)
record = mstats.compile(population)
logbook.record(gen=GENERATIONS, **record)


logbook.header = "gen", "fitness", "size"
logbook.chapters["fitness"].header = "min", "avg", "max"
logbook.chapters["size"].header = "min", "avg", "max"

print(logbook)


################
# Save Results #
################

print('Saving Results')
results = dict(population=population, logbook=logbook)
pickle.dump(results, open(os.path.join(RESULTS_DIRECTORY, datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + '.pkl'),'wb'))


