'''
Author:     James Hughes
Date:       June 12, 2020

Version:    0.1


Change Log:
    0.1 (June 12, 2020): 
        - Initial version.
    
End Change Log

Functions to generate statistics on the functions that have been tested. 

- Summary stats
---- Final susceptible
---- Max Infected
---- Total Infected (integrate/area under infected curve)
---- Final Removed (minus effective mitigations)
---- Total mitigations Used
-------- effective
-------- ineffective

- Comparing the distros (viz). 

- Average SEIR Curves 
---- Also plot effective mitigations and removed

'''

###########
# Imports #
###########

import matplotlib.pylab as plt
import numpy as np
import os
import pickle
import scipy
import scipy.stats

import evaluate
import snetwork

###########
# PARAMS  #
###########

RESULTS_DIRECTORY = "./function_tests/"
#FUNCTION = "mitigation_F1_False"       # CHANGE ME FOR SWITCHING OUT FUNCTIONS

###########

# Load the data from the pickle
def load_data(f_name):
    return pickle.load(open(os.path.join(RESULTS_DIRECTORY, f_name + ".pkl"), 'rb'))

# get the trends for all data
def get_all_trends(results, m):
    iterations = results[0]
    mitigations = results[1]

    iterations_trends = []
    mitigations_trends = []

    for i in range(len(iterations)):
        iterations_trends.append(model.build_trends(iterations[i])[0]['trends'])
        mitigations_trends.append(evaluate.mitigation_trends(mitigations[i])[0]['trends'])

    return np.array(iterations_trends), np.array(mitigations_trends)


# COnvert all teends to a single average one
def get_average_trends(iterations, mitigations):

    average_trends = {}
    average_trends[0] = []
    average_trends[1] = []
    average_trends[2] = []
    average_trends[3] = []
    average_trends['total'] = []
    average_trends['effective'] = []
    average_trends['ineffective'] = []

    # Could defo make this more general
    for i in range(len(iterations)): 
        average_trends[0].append(iterations[i]['node_count'][0])
        average_trends[1].append(iterations[i]['node_count'][1])
        average_trends[2].append(iterations[i]['node_count'][2])
        average_trends[3].append(iterations[i]['node_count'][3])
        average_trends['total'].append(mitigations[i]['node_count']['total'])
        average_trends['effective'].append(mitigations[i]['node_count']['effective'])
        average_trends['ineffective'].append(mitigations[i]['node_count']['ineffective'])

    average_trends[0] = np.average(average_trends[0], axis=0)
    average_trends[1] = np.average(average_trends[1], axis=0)
    average_trends[2] = np.average(average_trends[2], axis=0)
    average_trends[3] = np.average(average_trends[3], axis=0)
    average_trends['total'] = np.average(average_trends['total'], axis=0)
    average_trends['effective'] = np.average(average_trends['effective'], axis=0)
    average_trends['ineffective'] = np.average(average_trends['ineffective'], axis=0)

    return average_trends


# Extract Relevant Data for Summary Stats
def get_single_measures(results, m):
    iterations = results[0]
    mitigations = results[1]

    measures = {}
    measures['susceptible'] = []
    measures['max_infected'] = []
    measures['total_infected'] = []     # WARNING. This is NOT total, but area under curve
    measures['removed'] = []
    measures['mitigation'] = []
    measures['mitigation_effective'] = []
    measures['mitigation_ineffective'] = []

    
    for i in range(len(iterations)):
        sus, max_i, total_i, removed = evaluate.convert_iterations(iterations[i], m)
        total_mitigation, effective, ineffective = evaluate.convert_iterations_mitigations(mitigations[i])
        
        measures['susceptible'].append(sus)
        measures['max_infected'].append(max_i)
        measures['total_infected'].append(total_i)
        #measures['removed'].append(removed - effective)
        measures['removed'].append(removed)
        measures['mitigation'].append(total_mitigation)
        measures['mitigation_effective'].append(effective)
        measures['mitigation_ineffective'].append(ineffective)


    measures['susceptible'] = np.array(measures['susceptible'])
    measures['max_infected'] = np.array(measures['max_infected'])
    measures['total_infected'] = np.array(measures['total_infected'])
    measures['removed'] = np.array(measures['removed'])
    measures['mitigation'] = np.array(measures['mitigation'])
    measures['mitigation_effective'] = np.array(measures['mitigation_effective'])
    measures['mitigation_ineffective'] = np.array(measures['mitigation_ineffective'])

    return measures

# Compare distros
# MIGHT WANT THIS TO GENERATE ALL PLOTS?
def compare_distros(d1, d2, f1_name, f2_name, metric):

    pVal = scipy.stats.mannwhitneyu(d1, d2)
    print(pVal)
    
    plt.title('A Title')
    plt.xlabel(metric)
    plt.ylabel('Count')

    # Distros
    plt.hist(d1, color='b', alpha=0.75, label=f1_name)
    plt.axvline(np.median(d1), color='b', label=f1_name + ' Median')

    plt.hist(d2, color='r', alpha=0.75, label=f2_name)
    plt.axvline(np.median(d2), color='r', label=f2_name + ' Median')
    

    plt.legend()
    plt.show()


    return pVal




# Generate average epidemic curve plot
def average_epidemic_plot(results, m):
    pass



# Load Results
f1 = load_data('mitigation_F1_False')
random = load_data('mitigation_random_False')

model = snetwork.setup_network(0,0,0,0, size=500, edge_p=0.04)

m = get_single_measures(f1, model)
n = get_single_measures(random, model)
compare_distros(m['max_infected'], n['max_infected'], 'f1','rando','max_infected')
compare_distros(m['total_infected'], n['total_infected'], 'f1','rando','removed')
compare_distros(m['mitigation'], n['mitigation'], 'f1','rando','Mitigations')

i, m = get_all_trends(f1, model)
a = get_average_trends(i, m)

plt.plot(a[0])
plt.plot(a[1])
plt.plot(a[2])
plt.plot(a[3])
plt.plot(range(7, 140, 7), a['total'])
plt.show()

i, m = get_all_trends(random, model)
a = get_average_trends(i, m)

plt.plot(a[0])
plt.plot(a[1])
plt.plot(a[2])
plt.plot(a[3])
plt.plot(range(7, 140, 7), a['total'])
plt.show()


