'''
Author:     James Hughes
Date:       June 11, 2020

Version:    0.1


Change Log:
    0.1 (June 11, 2020): 
        - Initial version.
    

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


