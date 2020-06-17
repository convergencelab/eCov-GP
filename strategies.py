'''
Author:     James Hughes
Date:       June 11, 2020

Version:    0.3


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

        

End Change Log

Library of mitigation strategies. 
- Standard baseline vaccination strategies 
- Interesting generated functions


'''

###################
# Basic Idea Ones #
###################

# Vaccinate Noone
def mitigation_none(node_degree,
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
                        ):
    return False

# Assumes that the nodes being fed into function are shuffled
def mitigation_random(node_degree,
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
                        ):
    return True


# Mitigate nodes that are travelers only
#def mitigation_traveler(**kwargs):
#    return kwargs['traveler']

def mitigation_traveler(node_degree,
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
                        ):
    return traveler


def mitigation_degree5(node_degree,
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
                        ):
    return node_degree > 5

def mitigation_degree10(node_degree,
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
                        ):
    return node_degree > 10

def mitigation_degree15(node_degree,
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
                        ):
    return node_degree > 15

def mitigation_degree20(node_degree,
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
                        ):
    return node_degree > 20

def mitigation_degree25(node_degree,
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
                        ):
    return node_degree > 25

#####################
# Generated From AI #
#####################

def mitigation_F1(node_degree,
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
                        ):
    return traveler or ((14 - neighbour_infected) < (node_degree - 8))

def mitigation_F2(node_degree,
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
                        ):
    return node_degree > 10 and neighbour_infected > 3

def mitigation_F3(node_degree,
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
                        ):
    return neighbour_infected > 1

def mitigation_F4(node_degree,
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
                        ):
    return traveler and neighbour_infected > 5

# This one is weird. but whatever
def mitigation_F5(node_degree,
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
                        ):
    return num_mitigation < neighbour_infected

