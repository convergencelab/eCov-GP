'''
Author:     James Hughes
Date:       June 11, 2020

Version:    0.4


Change Log:
    0.1 (June 11, 2020): 
        - Initial version.
    
    0.2 (June 17, 2020):
        - Added degree 20 and 25 simple strategues
        - Turns out the average degree of a node was 20ish already        
        - Degree 5, 10 are more-or-less useless
        - Degree 15 is fine as some non-insignificant number of nodes had degree < 15        
        
    0.3 (June 17, 2020):
        - Added 4 more special functions found by GP (F2 -- f5)

    0.4 (November 25, 2020:
        - Can now load a serialized functions

        

End Change Log

Library of mitigation strategies. 
- Standard baseline vaccination strategies 
- Interesting generated functions


'''

import dill
import os
import pickle

from operator import *

RESULTS_DIRECTORY = "./output/"
SUB_DIRECTORY = ""

###################
# Basic Idea Ones #
###################

def if_then_else(in1, out1, out2):
    return out1 if in1 else out2


def protectedDiv(a, b):
    try:
        q = a / b
    except ZeroDivisionError:
        q = 1
        
    return q

# Vaccinate Noone
def mitigation_none(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return False

# Assumes that the nodes being fed into function are shuffled
def mitigation_random(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return True


# Mitigate nodes that are travelers only
#def mitigation_traveler(**kwargs):
#    return kwargs['traveler']

def mitigation_traveler(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return traveler


def mitigation_degree5(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return node_degree > 5

def mitigation_degree6(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return node_degree > 6

def mitigation_degree7(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return node_degree > 7

def mitigation_degree8(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return node_degree > 8

def mitigation_degree9(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return node_degree > 9




def mitigation_degree10(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return node_degree > 10

def mitigation_degree15(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return node_degree > 15

def mitigation_degree20(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return node_degree > 20

def mitigation_degree25(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return node_degree > 25

################################################################################################################################

#####################
#       OLD         #
#####################
# Generated From AI #
#####################

def mitigation_F1(nnode_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return traveler or ((14 - neighbour_infected) < (node_degree - 8))

def mitigation_F2(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return node_degree > 10 and neighbour_infected > 3

def mitigation_F3(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return neighbour_infected > 1

def mitigation_F4(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return traveler or neighbour_infected > 5

# This one is weird. but whatever
def mitigation_F5(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return num_mitigation < neighbour_infected


######################################################################################################################################

####################
#       NEW        #
####################
# Generated By AI  #
####################

# This worked well on all graphs
# with the sizes of:
# Nodes - 500
# Edges 1500 -- 2500 ish
# DEG - 2/3, 5.5 -- 8, 15 -- 70
# Dist - 1, 3 -- 4, 6ish
def mitigation_all_F1(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return node_degree > avg_neighbour_degree


#####################
# Generated For ER  #
#####################

def mitigation_ER_F1(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return True if node_degree > avg_neighbour_degree else traveler

######################################################################################################################################

######################
# Generated For NWS  #
######################

# Only found all 


######################################################################################################################################

#####################
# Generated For BA  #
#####################

def mitigation_BA_F1(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return traveler and (node_degree > 8) or node_degree > avg_neighbour_degree


def mitigation_BA_F2(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return traveler if (neighbour_infected > 9) else neighbour_susexp > 9

######################################################################################################################################

######################
# Generated For PCG  #
######################

def mitigation_PCG_F1(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):
    a = (node_degree * (page_rank + num_removed)) * (node_degree - 8)
    b = 8*(vertex_avg_dist + node_degree) + (vertex_avg_dist * num_susexp)
    
    c = node_degree * (vertex_avg_dist + num_removed) * (node_degree -8)
    d = cluster_coefficient + (8 * avg_dist) + (vertex_avg_dist * num_susexp)

    return (a > b) or (c > d)

def mitigation_PCG_F2(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):
    
    if node_degree < avg_neighbour_degree:
        a = node_degree < avg_neighbour_degree  # will be true
    else:
        a = avg_neighbour_degree < avg_degree

    return not a

def mitigation_PCG_F3(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):
    a = (node_degree * (node_degree + num_removed)) * (node_degree - 8)
    b = num_vert_shortest - avg_neighbour_degree + num_susexp + (vertex_avg_dist * avg_dist)
    c = (num_removed * num_removed) * (node_degree - (avg_degree + node_degree))

    return (a > b) or (c > vertex_avg_dist)


# 11-18-2020_20-59-25_122-compiled
def mitigation_PCG_F4(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):

    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '11-18-2020_20-59-25_122-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        )
    return to_vax


# 11-18-2020_20-59-25_365-compiled
def mitigation_PCG_F5(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):

    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '11-18-2020_20-59-25_365-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        )
    return to_vax


# 11-18-2020_21-16-02_100-compiled
def mitigation_PCG_F6(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):

    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '11-18-2020_21-16-02_100-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        )
    return to_vax

# 11-18-2020_21-16-02_704-compiled
def mitigation_PCG_F7(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):

    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '11-18-2020_21-16-02_704-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        )
    return to_vax

# 11-18-2020_21-16-02_757-compiled
def mitigation_PCG_F8(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):

    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '11-18-2020_21-16-02_757-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        )
    return to_vax


# 12-02-2020_23-55-14_27-compiled
def mitigation_PCG_F9(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):

    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '12-03-2020_01-31-23_806-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        )
    return to_vax

# 12-08-2020_10-36-23_81-compiled
def mitigation_PCG_F10(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):

    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '12-08-2020_10-36-23_81-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        )
    return to_vax

def mitigation_PCG_F11(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):

    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '12-08-2020_10-36-23_451-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        )
    return to_vax

def mitigation_PCG_F12(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):

    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '12-08-2020_18-17-53_664-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        )
    return to_vax

def mitigation_PCG_F99(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):

    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '12-08-2020_10-36-23_0-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        )
    return to_vax


#
# # got 128.5 2445.5
#
def mitigation_PCG_F101(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):
    '''
    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '12-20-2020_16-32-10_13-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        #cluster_coefficient,
                        #i,
                        )
    '''

    a = avg_neighbour_degree * ((2*avg_degree) - node_degree)
    
    if minimal_vertex_cover:
        b = avg_degree + num_removed + vertex_avg_dist
    else:
        b = avg_degree

    return a < b

# got 118 2495
def mitigation_PCG_F102(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):
    '''
    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '12-20-2020_16-32-10_13-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        #cluster_coefficient,
                        #i,
                        )
    '''

    return ((node_degree + num_infected) * node_degree) > (node_degree + num_removed + 650.8360370886498) - num_removed

    

# got 118.5 2452
def mitigation_PCG_F103(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):
    '''
    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '12-20-2020_16-32-10_13-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        #cluster_coefficient,
                        #i,
                        )
    '''
    return ((num_removed + neighbour_susexp + node_degree) * node_degree) > (neighbour_susexp + node_degree + 650.8360370886498 - neighbour_susexp)
    
# got 118.5 2468.5
def mitigation_PCG_F104(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):
    '''
    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '12-20-2020_16-32-10_13-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        #cluster_coefficient,
                        #i,
                        )
    '''
    return (num_susexp + 33 + neighbour_infected) < (neighbour_infected + vertex_avg_dist + cluster_coefficient + (33 * node_degree))

# got 121.5 2447.5
def mitigation_PCG_F105(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):
    '''
    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '12-20-2020_16-32-10_13-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        #cluster_coefficient,
                        #i,
                        )
    '''

    if neighbour_susexp > neighbour_infected:
        a = node_degree
    else:
        a = 0

    return node_degree - a < ((node_degree + neighbour_infected ) * 28) - (num_susexp - (node_degree - avg_neighbour_degree))


# got 109 2507
def mitigation_PCG_UA1(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):
    '''
    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '12-20-2020_16-32-10_13-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        #cluster_coefficient,
                        #i,
                        )
    '''

    return 414.777867048 <  ((node_degree + 15) * ((node_degree - 15) * avg_degree))

# got 119 2344.5
def mitigation_PCG_UA2(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):
    '''
    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '12-20-2020_16-32-10_13-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        #cluster_coefficient,
                        #i,
                        )
    '''

    return if_then_else(and_(eq(num_susexp, mul(87.4994455603728, 28)), eq(18, if_then_else(traveler, 599.3071641947356, num_vert_shortest))), gt(mul(node_degree, node_degree), mul(node_degree, 28)), gt(mul(node_degree, 28), num_susexp))

# got 116 2420.5
def mitigation_PCG_UA3(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        cluster_coefficient,
                        #i,
                        ):
    '''
    fName = os.path.join(RESULTS_DIRECTORY, SUB_DIRECTORY, '12-20-2020_16-32-10_13-compiled.dill')
    f = dill.load(open(fName, 'rb'))
    to_vax = f(node_degree,
                        avg_neighbour_degree,
                        neighbour_susexp, 
                        neighbour_infected,
                        #neighbour_removed,
                        traveler,
                        minimal_vertex_cover,
                        avg_degree,
                        avg_dist,
                        vertex_avg_dist,
                        #num_mitigation,
                        #mitigation,
                        num_susexp,
                        num_infected,
                        num_removed,
                        num_vert_shortest,
                        #s_dist_inf,
                        page_rank,
                        #cluster_coefficient,
                        #i,
                        )
    '''

    return if_then_else(and_(gt(sub(avg_degree, avg_neighbour_degree), sub(28, 28)), gt(mul(node_degree, 28), num_susexp)), False, gt(mul(node_degree, 28), num_susexp))


################################0######################################################################################################

###############################
# Generated For DUBLIN_07_15  #
###############################

def mitigation_DB_F1(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return (avg_neighbour_degree + neighbour_infected) < node_degree if node_degree > avg_neighbour_degree else avg_neighbour_degree < num_susexp


def mitigation_DB_F2(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return avg_neighbour_degree > neighbour_infected if node_degree > avg_neighbour_degree else False


def mitigation_DB_F3(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return neighbour_susexp > avg_neighbour_degree

def mitigation_DB_F4(node_degree,
                    avg_neighbour_degree,
                    neighbour_susexp, 
                    neighbour_infected,
                    #neighbour_removed,
                    traveler,
                    minimal_vertex_cover,
                    avg_degree,
                    avg_dist,
                    vertex_avg_dist,
                    #num_mitigation,
                    #mitigation,
                    num_susexp,
                    num_infected,
                    num_removed,
                    num_vert_shortest,
                    #s_dist_inf,
                    page_rank,
                    cluster_coefficient,
                    #i,
                        ):
    return node_degree > ((2*avg_neighbour_degree) - neighbour_susexp)




