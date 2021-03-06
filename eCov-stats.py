'''
Author:     James Hughes
Date:       June 12, 2020

Version:    0.5


Change Log:
    0.1 (June 12, 2020): 
        - Initial version.
    
    0.2 (June 16, 2020):
        - Plotting SEIR thing with vaccines and whatnot
        - Function to generate table row data
        - Funcitonality to generate table for all strategies 
        - Made a 3/removed prime thing to keep track of removed - effective mitigations
        
    0.3 (June 17, 2020):
        - Added functions to generate tables automatically
            - Results tables
            - p-val table comparing static and dynamic

    0.4 (July 15, 2020):
        - Added constants for node status
        - Fixed node status issue (had originally swapped exposed and infected)

    0.5 (November 3, 2020):
        - Added functions to test the 'break' results

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




MEASURE_EVERY = 7
# ER
FUNCTIONS_STATIC_ER = [
            'mitigation_none_ER_False',
            'mitigation_random_ER_False',
            'mitigation_traveler_ER_False',
            'mitigation_degree5_ER_False',
            'mitigation_degree6_ER_False',
            'mitigation_degree7_ER_False',
            'mitigation_degree8_ER_False',
            'mitigation_degree9_ER_False',
            'mitigation_degree10_ER_False',
            'mitigation_all_F1_ER_False',
            'mitigation_PCG_F1_ER_False',
            'mitigation_PCG_F2_ER_False',
            'mitigation_PCG_F3_ER_False',
            ]       # CHANGE ME FOR SWITCHING OUT FUNCTIONS


FUNCTIONS_NONSTATIC_ER = [
            'mitigation_none_ER_True',
            'mitigation_random_ER_True',
            'mitigation_traveler_ER_True',
            'mitigation_degree5_ER_True',
            'mitigation_degree6_ER_True',
            'mitigation_degree7_ER_True',
            'mitigation_degree8_ER_True',
            'mitigation_degree9_ER_True',
            'mitigation_degree10_ER_True',
            'mitigation_all_F1_ER_True',
            ]       # CHANGE ME FOR SWITCHING OUT FUNCTIONS


# NWS
FUNCTIONS_STATIC_NWS = [
            'mitigation_none_NWS_False',
            'mitigation_random_NWS_False',
            'mitigation_traveler_NWS_False',
            'mitigation_degree5_NWS_False',
            'mitigation_degree6_NWS_False',
            'mitigation_degree7_NWS_False',
            'mitigation_degree8_NWS_False',
            'mitigation_degree9_NWS_False',
            'mitigation_degree10_NWS_False',
            'mitigation_all_F1_NWS_False',
            'mitigation_PCG_F1_NWS_False',
            'mitigation_PCG_F2_NWS_False',
            'mitigation_PCG_F3_NWS_False',
            ]       # CHANGE ME FOR SWITCHING OUT FUNCTIONS


FUNCTIONS_NONSTATIC_NWS = [
            'mitigation_none_NWS_True',
            'mitigation_random_NWS_True',
            'mitigation_traveler_NWS_True',
            'mitigation_degree5_NWS_True',
            'mitigation_degree6_NWS_True',
            'mitigation_degree7_NWS_True',
            'mitigation_degree8_NWS_True',
            'mitigation_degree9_NWS_True',
            'mitigation_degree10_NWS_True',
            'mitigation_all_F1_NWS_True',
            'mitigation_PCG_F1_NWS_True',
            'mitigation_PCG_F2_NWS_True',
            'mitigation_PCG_F3_NWS_True',
            ]       # CHANGE ME FOR SWITCHING OUT FUNCTIONS


# BA
FUNCTIONS_STATIC_BA = [
            'mitigation_none_BA_False',
            'mitigation_random_BA_False',
            'mitigation_traveler_BA_False',
            'mitigation_degree5_BA_False',
            'mitigation_degree6_BA_False',
            'mitigation_degree7_BA_False',
            'mitigation_degree8_BA_False',
            'mitigation_degree9_BA_False',
            'mitigation_degree10_BA_False',
            'mitigation_all_F1_BA_False',
            'mitigation_PCG_F1_BA_False',
            'mitigation_PCG_F2_BA_False',
            'mitigation_PCG_F3_BA_False',
            ]       # CHANGE ME FOR SWITCHING OUT FUNCTIONS


FUNCTIONS_NONSTATIC_BA = [
            'mitigation_none_BA_True',
            'mitigation_random_BA_True',
            'mitigation_traveler_BA_True',
            'mitigation_degree5_BA_True',
            'mitigation_degree6_BA_True',
            'mitigation_degree7_BA_True',
            'mitigation_degree8_BA_True',
            'mitigation_degree9_BA_True',
            'mitigation_degree10_BA_True',
            'mitigation_all_F1_BA_True',
            'mitigation_PCG_F1_BA_True',
            'mitigation_PCG_F2_BA_True',
            'mitigation_PCG_F3_BA_True',
            ]       # CHANGE ME FOR SWITCHING OUT FUNCTIONS


FUNCTIONS_STATIC_PCG = [
            'mitigation_none_PCG_False',
            'mitigation_random_PCG_False',
            'mitigation_traveler_PCG_False',
            'mitigation_degree5_PCG_False',
            'mitigation_degree6_PCG_False',
            'mitigation_degree7_PCG_False',
            'mitigation_degree8_PCG_False',
            'mitigation_degree9_PCG_False',
            'mitigation_degree10_PCG_False',
            'mitigation_all_F1_PCG_False',
            'mitigation_PCG_F1_PCG_False',
            'mitigation_PCG_F2_PCG_False',
            'mitigation_PCG_F3_PCG_False',
            'mitigation_PCG_F4_PCG_False',
            'mitigation_PCG_F5_PCG_False',
            'mitigation_PCG_F6_PCG_False',
            'mitigation_PCG_F7_PCG_False',
            'mitigation_PCG_F8_PCG_False',
            'mitigation_PCG_F9_PCG_False',
            'mitigation_PCG_F10_PCG_False',
            'mitigation_PCG_F11_PCG_False',
            'mitigation_PCG_F12_PCG_False',
            'mitigation_PCG_F99_PCG_False',
            'mitigation_PCG_F101_PCG_False',
            'mitigation_PCG_F102_PCG_False',
            'mitigation_PCG_F103_PCG_False',
            'mitigation_PCG_F104_PCG_False',
            'mitigation_PCG_F105_PCG_False',
            'mitigation_PCG_UA1_PCG_False',
            'mitigation_PCG_UA2_PCG_False',
            'mitigation_PCG_UA3_PCG_False',
            ]       # CHANGE ME FOR SWITCHING OUT FUNCTIONS


FUNCTIONS_NONSTATIC_PCG = [
            'mitigation_none_PCG_True',
            'mitigation_random_PCG_True',
            'mitigation_traveler_PCG_True',
            'mitigation_degree5_PCG_True',
            'mitigation_degree6_PCG_True',
            'mitigation_degree7_PCG_True',
            'mitigation_degree8_PCG_True',
            'mitigation_degree9_PCG_True',
            'mitigation_degree10_PCG_True',
            'mitigation_all_F1_PCG_True',
            'mitigation_PCG_F1_PCG_True',
            'mitigation_PCG_F2_PCG_True',
            'mitigation_PCG_F3_PCG_True',
            'mitigation_PCG_F4_PCG_True',
            'mitigation_PCG_F5_PCG_True',
            'mitigation_PCG_F6_PCG_True',
            'mitigation_PCG_F7_PCG_True',
            'mitigation_PCG_F8_PCG_True',
            'mitigation_PCG_F9_PCG_True',
            'mitigation_PCG_F10_PCG_True',
            'mitigation_PCG_F11_PCG_True',
            'mitigation_PCG_F12_PCG_True',
            'mitigation_PCG_F99_PCG_True',
            'mitigation_PCG_F101_PCG_True',
            'mitigation_PCG_F102_PCG_True',
            'mitigation_PCG_F103_PCG_True',
            'mitigation_PCG_F104_PCG_True',
            'mitigation_PCG_F105_PCG_True',
            'mitigation_PCG_UA1_PCG_True',
            'mitigation_PCG_UA2_PCG_True',
            'mitigation_PCG_UA3_PCG_True',
            ]       # CHANGE ME FOR SWITCHING OUT FUNCTIONS


# DUB15
FUNCTIONS_STATIC_DB15 = [
            'mitigation_none_DB15_False',
            'mitigation_random_DB15_False',
            'mitigation_traveler_DB15_False',
            'mitigation_degree5_DB15_False',
            'mitigation_degree6_DB15_False',
            'mitigation_degree7_DB15_False',
            'mitigation_degree8_DB15_False',
            'mitigation_degree9_DB15_False',
            'mitigation_degree10_DB15_False',
            'mitigation_all_F1_DB15_False',
            'mitigation_PCG_F1_DB15_False',
            'mitigation_PCG_F2_DB15_False',
            'mitigation_PCG_F3_DB15_False',
            ]       # CHANGE ME FOR SWITCHING OUT FUNCTIONS




STATUS_SUSCEPTIBLE = 0
STATUS_EXPOSED = 2
STATUS_INFECTED = 1
STATUS_REMOVED = 3
STATUS_MITIGATED = 4



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




# C0nvert all teends to a single average one
def get_average_trends(iterations, mitigations, mitigate_period=7):

    average_trends = {}
    average_trends[STATUS_SUSCEPTIBLE] = []
    average_trends[STATUS_EXPOSED] = []
    average_trends[STATUS_INFECTED] = []
    average_trends[STATUS_REMOVED] = []
    average_trends['3_p'] = []
    average_trends['total'] = []
    average_trends['effective'] = []
    average_trends['ineffective'] = []

    # Could defo make this more general
    for i in range(len(iterations)): 
        average_trends[STATUS_SUSCEPTIBLE].append(iterations[i]['node_count'][STATUS_SUSCEPTIBLE])
        average_trends[STATUS_EXPOSED].append(iterations[i]['node_count'][STATUS_EXPOSED])
        average_trends[STATUS_INFECTED].append(iterations[i]['node_count'][STATUS_INFECTED])
        average_trends[STATUS_REMOVED].append(iterations[i]['node_count'][STATUS_REMOVED])
        average_trends['total'].append(mitigations[i]['node_count']['total'])
        average_trends['effective'].append(mitigations[i]['node_count']['effective'])
        average_trends['ineffective'].append(mitigations[i]['node_count']['ineffective'])

    average_trends[STATUS_SUSCEPTIBLE] = np.average(average_trends[STATUS_SUSCEPTIBLE], axis=0)
    average_trends[STATUS_EXPOSED] = np.average(average_trends[STATUS_EXPOSED], axis=0)
    average_trends[STATUS_INFECTED] = np.average(average_trends[STATUS_INFECTED], axis=0)
    average_trends[STATUS_REMOVED] = np.average(average_trends[STATUS_REMOVED], axis=0)
    average_trends['total'] = np.average(average_trends['total'], axis=0)
    average_trends['effective'] = np.average(average_trends['effective'], axis=0)
    average_trends['ineffective'] = np.average(average_trends['ineffective'], axis=0)

    # 3_PRIME
    # Since we only have 1 mitigate count for every mitigation_period, we need to count carefully
    for i in range(len(average_trends[STATUS_REMOVED])):
        if(i < mitigate_period):
            average_trends['3_p'].append(average_trends[STATUS_REMOVED][i])
        else:
            average_trends['3_p'].append(average_trends[STATUS_REMOVED][i] - average_trends['effective'][(i - mitigate_period)//mitigate_period])

    # Make the 3' an array
    average_trends['3_p'] = np.array(average_trends['3_p'])
    return average_trends

# Generate average epidemic curve plot
def average_epidemic_plot(results, fName, mitigate_period=7):

    plt.bar(range(mitigate_period, len(results[0]), mitigate_period), results['total'], width=mitigate_period, align='edge', color='m', alpha=0.2, label='Total Mitigations')
    plt.bar(range(mitigate_period, len(results[0]), mitigate_period), results['effective'], width=mitigate_period, align='edge', color='m', alpha=0.4, label='Effective Mitigations')
    plt.bar(np.arange(mitigate_period, len(results[0]), mitigate_period), results['ineffective'], width=mitigate_period, align='edge', color='m', alpha=0.6, label='Ineffective Mitigations')
    plt.plot(results[STATUS_SUSCEPTIBLE], color='b', label='Susceptible')
    plt.plot(results[STATUS_EXPOSED], color='g', label='Exposed')
    plt.plot(results[STATUS_INFECTED], color='y', label='Infected')
    plt.plot(results[STATUS_REMOVED], color='r', label='Removed')
    plt.plot(results['3_p'], color='r', linestyle='--', label='Removed\'')

    plt.title(fName)
    plt.ylabel('Count')
    plt.xlabel('Days')
    plt.legend(loc=1, fontsize=8)
    plt.show()


# Extract Relevant Data for Summary Stats
def get_single_measures(results, m):
    iterations = results[0]
    mitigations = results[1]

    measures = {}
    measures['susceptible'] = []
    measures['max_infected'] = []
    measures['total_infected'] = []     # WARNING. This is NOT total, but area under curve
    measures['removed'] = []
    measures['removed_p'] = []
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
        measures['removed_p'].append(removed - effective)
        measures['mitigation'].append(total_mitigation)
        measures['mitigation_effective'].append(effective)
        measures['mitigation_ineffective'].append(ineffective)


    measures['susceptible'] = np.array(measures['susceptible'])
    measures['max_infected'] = np.array(measures['max_infected'])
    measures['total_infected'] = np.array(measures['total_infected'])
    measures['removed'] = np.array(measures['removed'])
    measures['removed_p'] = np.array(measures['removed_p'])
    measures['mitigation'] = np.array(measures['mitigation'])
    measures['mitigation_effective'] = np.array(measures['mitigation_effective'])
    measures['mitigation_ineffective'] = np.array(measures['mitigation_ineffective'])

    return measures

# Generate a function's summary statistics for a row's in a table
def get_function_summary_statistics(measures, measure_keys):
    s = ''

    for k in measure_keys:
        s += ' \t& ' + str(round(np.median(measures[k]), 2)) + ' & ($\\pm$ ' + str(round(scipy.stats.iqr(measures[k])/2, 2)) + ')'
    
    return s + '\t\\\\\n'

# summary statistics table
def generate_summary_statistic_table(functions, model, measure_keys):
    s = ''

    for f in range(len(functions)):
        data = load_data(functions[f])

        measures = get_single_measures(data, model)
        s += functions[f]
        s += get_function_summary_statistics(measures, measure_keys)

    return s


# Generate a function's summary statistics for a row's in a table
def compare_distros_p_vals(measures1, measures2, measure_keys):
    s = ''

    for k in measure_keys:
        try:
            #s += ' \t& ' + str(round(scipy.stats.mannwhitneyu(measures1[k], measures2[k])[1]), 3))
            s += ' \t& ' + '{:.2e}'.format(scipy.stats.mannwhitneyu(measures1[k], measures2[k])[1])
        except:
            s += ' \t& ' + ' --- '

    return s + '\t\\\\\n'


# p-val statistics table
def generate_p_val_table(static, dynamic, model, measure_keys):
    s = ''

    for f in range(len(static)):
        data_s = load_data(static[f])
        data_d = load_data(dynamic[f])

        measures_s = get_single_measures(data_s, model)
        measures_d = get_single_measures(data_d, model)

        s += compare_distros_p_vals(measures_s, measures_d, measure_keys)

    return s


def generate_p_val_matrix(functions, function_names, indices, measure, measure_key, model):
    
    # Get relevant info
    f_data = []
    for ind in indices:
        f_data.append(get_single_measures(load_data(functions[ind]), model))


    # Generate p-val matrix
    pVals = []
    for i in range(len(f_data)):
        pVal_row = []
        for j in range(len(f_data)):
            pVal_row.append(scipy.stats.mannwhitneyu(f_data[i][measure_key], f_data[j][measure_key])[1])    
            #pVal_row.append(scipy.stats.ttest_ind(f_data[i][measure_key], f_data[j][measure_key])[1])    
        pVals.append(pVal_row)

    pVals = np.array(pVals)
    plt.matshow(pVals)

    for (i, j), z in np.ndenumerate(pVals):
        if z < 0.1:
            plt.text(j, i, '{:0.2e}'.format(z), ha='center', va='center', color='w')
        else:    
            plt.text(j, i, '{:0.2e}'.format(z), ha='center', va='center')

    plt.title(measure)
    plt.xticks(range(len(function_names)), function_names)
    plt.yticks(range(len(function_names)), function_names, rotation = 90)

    plt.colorbar(label='Mann-Whitney U Test p-Value')



    plt.show()



# Compare distros
# MIGHT WANT THIS TO GENERATE ALL PLOTS?
def compare_distros(d1, d2, f1_name, f2_name, metric):

    pVal = scipy.stats.mannwhitneyu(d1, d2)
    print(pVal)
    
    plt.title(metric + ': ' + f1_name + ' vs. ' + f2_name)
    plt.xlabel(metric)
    plt.ylabel('Count')

    # Get good number of bins
    bins = np.histogram(np.hstack((d1,d2)), bins=25)[1]

    # Plot Distros
    plt.hist(d1, color='b', alpha=0.66, label=f1_name, bins=bins)
    plt.axvline(np.median(d1), color='b', label=f1_name + ' Median (' + str(round(np.median(d1), 2)) + ')')

    plt.hist(d2, color='r', alpha=0.66, label=f2_name, bins=bins)
    plt.axvline(np.median(d2), color='r', label=f2_name + ' Median (' + str(round(np.median(d2), 2)) + ')')
    
    plt.legend()
    plt.show()

    return pVal


# This is gross and hacked together
# Should improve this later
def break_function(mitigation, graph, static, values, key):
    medians = []
    iqrs = []
    for v in values:
        # Load data
        data = load_data(mitigation + '_' + graph + '_' + str(v) + '_' + str(static))
        # Format the data nice
        measures = get_single_measures(data, model)
        medians.append(np.median(measures[key]))
        iqrs.append(scipy.stats.iqr(measures[key])/2)

    return medians, iqrs


def do_grow():
    ## Max Infected ##
    '''
    # ER NON Static
    m, i = break_function('mitigation_all_F1', 'ER', True, EDGE_ps, 'max_infected')
    #n, j = break_function('../function_tests_break/mitigation_none', 'ER', True, EDGE_ps, 'max_infected')
    n, j = break_function('../function_tests_grow/mitigation_none', 'ER', True, EDGE_ps, 'max_infected')
    o, k = break_function('mitigation_random', 'ER', True, EDGE_ps, 'max_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('ER NONStatic --- Max Infected')
    plt.xlabel('Edge Connection Probabilities')
    plt.xticks(range(len(EDGE_ps)), EDGE_ps)
    plt.ylabel('Max Infected')
    plt.show()


    # NWS NON Static
    m, i = break_function('mitigation_all_F1', 'NWS', True, DROPs, 'max_infected')
    #n, j = break_function('../function_tests_break/mitigation_none', 'NWS', True, DROPs, 'max_infected')
    n, j = break_function('../function_tests_grow/mitigation_none', 'NWS', True, DROPs, 'max_infected')
    o, k = break_function('mitigation_random', 'NWS', True, DROPs, 'max_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('NWS NONStatic --- Max Infected')
    plt.xlabel('Drops')
    plt.xticks(range(len(m)), DROPs)
    plt.ylabel('Max Infected')
    plt.show()
    '''
    # BA NON Static
    m, i = break_function('mitigation_all_F1', 'BA', True, GRAPH_SIZEs, 'max_infected')
    #n, j = break_function('../function_tests_break/mitigation_none', 'BA', True, Ms, 'max_infected')
    n, j = break_function('mitigation_none', 'BA', True, GRAPH_SIZEs, 'max_infected')
    o, k = break_function('mitigation_random', 'BA', True, GRAPH_SIZEs, 'max_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    print('F1', (m[-1] - m[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('Random', (o[-1] - o[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('None', (n[-1] - n[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('BA NONStatic --- Max Infected')
    plt.xlabel('M')
    plt.xlabel('|V|')
    #plt.xticks(range(len(m)), Ms)
    plt.xticks(range(len(m)), GRAPH_SIZEs)
    plt.ylabel('Max Infected')
    plt.show()

    # PCG NON Static
    m, i = break_function('mitigation_all_F1', 'PCG', True, GRAPH_SIZEs, 'max_infected')
    #n, j = break_function('../function_tests_break/mitigation_none', 'BA', True, Ms, 'max_infected')
    n, j = break_function('mitigation_none', 'PCG', True, GRAPH_SIZEs, 'max_infected')
    o, k = break_function('mitigation_random', 'PCG', True, GRAPH_SIZEs, 'max_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    print('F1', (m[-1] - m[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('Random', (o[-1] - o[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('None', (n[-1] - n[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    # PCG new stuff
    m, i = break_function('mitigation_PCG_F1', 'PCG', True, GRAPH_SIZEs, 'max_infected')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F2', 'PCG', True, GRAPH_SIZEs, 'max_infected')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F2')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F3', 'PCG', True, GRAPH_SIZEs, 'max_infected')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F3')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    # End PCG New Stuff

    plt.legend()
    plt.title('PCG NONStatic --- Max Infected')
    plt.xlabel('|V|')
    #plt.xticks(range(len(m)), Ms)
    plt.xticks(range(len(m)), GRAPH_SIZEs)
    plt.ylabel('Max Infected')
    plt.show()


    # PCG NON Static
    m, i = break_function('mitigation_all_F1', 'PCG', True, GRAPH_SIZEs, 'max_infected')
    #n, j = break_function('../function_tests_break/mitigation_none', 'BA', True, Ms, 'total_infected')
    n, j = break_function('mitigation_none', 'PCG', True, GRAPH_SIZEs, 'max_infected')
    o, k = break_function('mitigation_random', 'PCG', True, GRAPH_SIZEs, 'max_infected')
    m = np.array(m)/[500, 1000, 1500, 2000]
    n = np.array(n)/[500, 1000, 1500, 2000]
    o = np.array(o)/[500, 1000, 1500, 2000]
    i = np.array(i)/[500, 1000, 1500, 2000]
    j = np.array(j)/[500, 1000, 1500, 2000]
    k = np.array(k)/[500, 1000, 1500, 2000]

    print('F1', (m[-1] - m[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('Random', (o[-1] - o[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('None', (n[-1] - n[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    # PCG new stuff
    m, i = break_function('mitigation_PCG_F1', 'PCG', True, GRAPH_SIZEs, 'max_infected')
    m = np.array(m)/[500, 1000, 1500, 2000]
    i = np.array(i)/[500, 1000, 1500, 2000]
    plt.plot(m, label='PCG-F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F2', 'PCG', True, GRAPH_SIZEs, 'max_infected')
    m = np.array(m)/[500, 1000, 1500, 2000]
    i = np.array(i)/[500, 1000, 1500, 2000]
    plt.plot(m, label='PCG-F2')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F3', 'PCG', True, GRAPH_SIZEs, 'max_infected')
    m = np.array(m)/[500, 1000, 1500, 2000]
    i = np.array(i)/[500, 1000, 1500, 2000]
    plt.plot(m, label='PCG-F3')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    # End PCG New Stuff

    plt.legend()
    plt.title('PCG NONStatic --- Max Infected')
    #plt.xlabel('Ms')
    plt.xlabel('|V|')
    #plt.xticks(range(len(m)), Ms)
    plt.xticks(range(len(m)), GRAPH_SIZEs)
    plt.ylabel('Max Infected/|V|')
    plt.show()


    #################################
    ## Total Infected ##
    '''
    # ER NON Static
    m, i = break_function('mitigation_all_F1', 'ER', True, EDGE_ps, 'total_infected')
    #n, j = break_function('../function_tests_break/mitigation_none', 'ER', True, EDGE_ps, 'total_infected')
    n, j = break_function('../function_tests_grow/mitigation_none', 'ER', True, EDGE_ps, 'total_infected')
    o, k = break_function('mitigation_random', 'ER', True, EDGE_ps, 'total_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('ER NONStatic --- Total Infected')
    plt.xlabel('Edge Connection Probabilities')
    plt.xticks(range(len(EDGE_ps)), EDGE_ps)
    plt.ylabel('total_infected')
    plt.show()


    # NWS NON Static
    m, i = break_function('mitigation_all_F1', 'NWS', True, DROPs, 'total_infected')
    #n, j = break_function('../function_tests_break/mitigation_none', 'NWS', True, DROPs, 'total_infected')
    n, j = break_function('../function_tests_grow/mitigation_none', 'NWS', True, DROPs, 'total_infected')
    o, k = break_function('mitigation_random', 'NWS', True, DROPs, 'total_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('NWS NONStatic --- Total Infected')
    plt.xlabel('Drops')
    plt.xticks(range(len(m)), DROPs)
    plt.ylabel('total_infected')
    plt.show()
    '''
    # BA NON Static
    m, i = break_function('mitigation_all_F1', 'BA', True, GRAPH_SIZEs, 'total_infected')
    #n, j = break_function('../function_tests_break/mitigation_none', 'BA', True, Ms, 'total_infected')
    n, j = break_function('mitigation_none', 'BA', True, GRAPH_SIZEs, 'total_infected')
    o, k = break_function('mitigation_random', 'BA', True, GRAPH_SIZEs, 'total_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    print('F1', (m[-1] - m[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('Random', (o[-1] - o[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('None', (n[-1] - n[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('BA NONStatic --- Total Infected')
    #plt.xlabel('Ms')
    plt.xlabel('|V|')
    #plt.xticks(range(len(m)), Ms)
    plt.xticks(range(len(m)), GRAPH_SIZEs)
    plt.ylabel('Total Infected')
    plt.show()


    # PCG NON Static
    m, i = break_function('mitigation_all_F1', 'PCG', True, GRAPH_SIZEs, 'total_infected')
    #n, j = break_function('../function_tests_break/mitigation_none', 'BA', True, Ms, 'total_infected')
    n, j = break_function('mitigation_none', 'PCG', True, GRAPH_SIZEs, 'total_infected')
    o, k = break_function('mitigation_random', 'PCG', True, GRAPH_SIZEs, 'total_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    print('F1', (m[-1] - m[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('Random', (o[-1] - o[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('None', (n[-1] - n[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    # PCG new stuff
    m, i = break_function('mitigation_PCG_F1', 'PCG', True, GRAPH_SIZEs, 'total_infected')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F2', 'PCG', True, GRAPH_SIZEs, 'total_infected')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F2')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F3', 'PCG', True, GRAPH_SIZEs, 'total_infected')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F3')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    # End PCG New Stuff

    plt.legend()
    plt.title('PCG NONStatic --- Total Infected')
    #plt.xlabel('Ms')
    plt.xlabel('|V|')
    #plt.xticks(range(len(m)), Ms)
    plt.xticks(range(len(m)), GRAPH_SIZEs)
    plt.ylabel('Total Infected')
    plt.show()

    # PCG NON Static
    m, i = break_function('mitigation_all_F1', 'PCG', True, GRAPH_SIZEs, 'total_infected')
    #n, j = break_function('../function_tests_break/mitigation_none', 'BA', True, Ms, 'total_infected')
    n, j = break_function('mitigation_none', 'PCG', True, GRAPH_SIZEs, 'total_infected')
    o, k = break_function('mitigation_random', 'PCG', True, GRAPH_SIZEs, 'total_infected')
    m = np.array(m)/[500, 1000, 1500, 2000]
    n = np.array(n)/[500, 1000, 1500, 2000]
    o = np.array(o)/[500, 1000, 1500, 2000]
    i = np.array(i)/[500, 1000, 1500, 2000]
    j = np.array(j)/[500, 1000, 1500, 2000]
    k = np.array(k)/[500, 1000, 1500, 2000]

    print('F1', (m[-1] - m[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('Random', (o[-1] - o[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('None', (n[-1] - n[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    # PCG new stuff
    m, i = break_function('mitigation_PCG_F1', 'PCG', True, GRAPH_SIZEs, 'total_infected')
    m = np.array(m)/[500, 1000, 1500, 2000]
    i = np.array(i)/[500, 1000, 1500, 2000]
    plt.plot(m, label='PCG-F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F2', 'PCG', True, GRAPH_SIZEs, 'total_infected')
    m = np.array(m)/[500, 1000, 1500, 2000]
    i = np.array(i)/[500, 1000, 1500, 2000]
    plt.plot(m, label='PCG-F2')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F3', 'PCG', True, GRAPH_SIZEs, 'total_infected')
    m = np.array(m)/[500, 1000, 1500, 2000]
    i = np.array(i)/[500, 1000, 1500, 2000]
    plt.plot(m, label='PCG-F3')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    # End PCG New Stuff

    plt.legend()
    plt.title('PCG NONStatic --- Total Infected')
    #plt.xlabel('Ms')
    plt.xlabel('|V|')
    #plt.xticks(range(len(m)), Ms)
    plt.xticks(range(len(m)), GRAPH_SIZEs)
    plt.ylabel('Total Infected/|V|')
    plt.show()

    ################
    ## Mitigations Used ##
    '''
    # ER NON Static
    m, i = break_function('mitigation_all_F1', 'ER', True, EDGE_ps, 'mitigation')
    #n, j = break_function('../function_tests_break/mitigation_none', 'ER', True, EDGE_ps, 'mitigation')
    n, j = break_function('../function_tests_grow/mitigation_none', 'ER', True, EDGE_ps, 'mitigation')
    o, k = break_function('mitigation_random', 'ER', True, EDGE_ps, 'mitigation')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('ER NONStatic --- Mitigation Used')
    plt.xlabel('Edge Connection Probabilities')
    plt.xticks(range(len(EDGE_ps)), EDGE_ps)
    plt.ylabel('Mitigations Used')
    plt.show()


    # NWS NON Static
    m, i = break_function('mitigation_all_F1', 'NWS', True, DROPs, 'mitigation')
    #n, j = break_function('../function_tests_break/mitigation_none', 'NWS', True, DROPs, 'mitigation')
    n, j = break_function('../function_tests_grow/mitigation_none', 'NWS', True, DROPs, 'mitigation')
    o, k = break_function('mitigation_random', 'NWS', True, DROPs, 'mitigation')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('NWS NONStatic --- Mitigation Used')
    plt.xlabel('Drops')
    plt.xticks(range(len(m)), DROPs)
    plt.ylabel('Mitigation Used')
    plt.show()
    '''
    # BA NON Static
    m, i = break_function('mitigation_all_F1', 'BA', True, GRAPH_SIZEs, 'mitigation')
    #n, j = break_function('../function_tests_break/mitigation_none', 'BA', True, Ms, 'mitigation')
    n, j = break_function('mitigation_none', 'BA', True, GRAPH_SIZEs, 'mitigation')
    o, k = break_function('mitigation_random', 'BA', True, GRAPH_SIZEs, 'mitigation')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    print('F1', (m[-1] - m[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('Random', (o[-1] - o[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('None', (n[-1] - n[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('BA NONStatic --- Mitigation Used')
    #plt.xlabel('M')
    plt.xlabel('|V|')
    #plt.xticks(range(len(m)), Ms)
    plt.xticks(range(len(m)), GRAPH_SIZEs)
    plt.ylabel('Mitigation Used')
    plt.show()

    # PCG NON Static
    m, i = break_function('mitigation_all_F1', 'PCG', True, GRAPH_SIZEs, 'mitigation')
    #n, j = break_function('../function_tests_break/mitigation_none', 'BA', True, Ms, 'mitigation')
    n, j = break_function('mitigation_none', 'PCG', True, GRAPH_SIZEs, 'mitigation')
    o, k = break_function('mitigation_random', 'PCG', True, GRAPH_SIZEs, 'mitigation')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    print('F1', (m[-1] - m[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('Random', (o[-1] - o[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('None', (n[-1] - n[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    # PCG new stuff
    m, i = break_function('mitigation_PCG_F1', 'PCG', True, GRAPH_SIZEs, 'mitigation')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F2', 'PCG', True, GRAPH_SIZEs, 'mitigation')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F2')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F3', 'PCG', True, GRAPH_SIZEs, 'mitigation')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F3')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    # End PCG New Stuff

    plt.legend()
    plt.title('PCG NONStatic --- Mitigation Used')
    #plt.xlabel('M')
    plt.xlabel('|V|')
    #plt.xticks(range(len(m)), Ms)
    plt.xticks(range(len(m)), GRAPH_SIZEs)
    plt.ylabel('Mitigation Used')
    plt.show()

    # PCG NON Static
    m, i = break_function('mitigation_all_F1', 'PCG', True, GRAPH_SIZEs, 'mitigation')
    #n, j = break_function('../function_tests_break/mitigation_none', 'BA', True, Ms, 'total_infected')
    n, j = break_function('mitigation_none', 'PCG', True, GRAPH_SIZEs, 'mitigation')
    o, k = break_function('mitigation_random', 'PCG', True, GRAPH_SIZEs, 'mitigation')
    m = np.array(m)/[500, 1000, 1500, 2000]
    n = np.array(n)/[500, 1000, 1500, 2000]
    o = np.array(o)/[500, 1000, 1500, 2000]
    i = np.array(i)/[500, 1000, 1500, 2000]
    j = np.array(j)/[500, 1000, 1500, 2000]
    k = np.array(k)/[500, 1000, 1500, 2000]

    print('F1', (m[-1] - m[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('Random', (o[-1] - o[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))
    print('None', (n[-1] - n[0])/(GRAPH_SIZEs[-1]-GRAPH_SIZEs[0]))

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    # PCG new stuff
    m, i = break_function('mitigation_PCG_F1', 'PCG', True, GRAPH_SIZEs, 'mitigation')
    m = np.array(m)/[500, 1000, 1500, 2000]
    i = np.array(i)/[500, 1000, 1500, 2000]
    plt.plot(m, label='PCG-F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F2', 'PCG', True, GRAPH_SIZEs, 'mitigation')
    m = np.array(m)/[500, 1000, 1500, 2000]
    i = np.array(i)/[500, 1000, 1500, 2000]
    plt.plot(m, label='PCG-F2')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F3', 'PCG', True, GRAPH_SIZEs, 'mitigation')
    m = np.array(m)/[500, 1000, 1500, 2000]
    i = np.array(i)/[500, 1000, 1500, 2000]
    plt.plot(m, label='PCG-F3')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    # End PCG New Stuff

    plt.legend()
    plt.title('PCG NONStatic --- Mitigation Used')
    #plt.xlabel('Ms')
    plt.xlabel('|V|')
    #plt.xticks(range(len(m)), Ms)
    plt.xticks(range(len(m)), GRAPH_SIZEs)
    plt.ylabel('Mitigation Used/|V|')
    plt.show()


def do_break():
    ## Max Infected ##

    # ER NON Static
    m, i = break_function('mitigation_all_F1', 'ER', True, EDGE_ps, 'max_infected')
    n, j = break_function('../function_tests_break/mitigation_none', 'ER', True, EDGE_ps, 'max_infected')
    o, k = break_function('mitigation_random', 'ER', True, EDGE_ps, 'max_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('ER NONStatic --- Max Infected')
    plt.xlabel('Edge Connection Probabilities')
    plt.xticks(range(len(EDGE_ps)), EDGE_ps)
    plt.ylabel('Max Infected')
    plt.show()


    # NWS NON Static
    m, i = break_function('mitigation_all_F1', 'NWS', True, DROPs, 'max_infected')
    n, j = break_function('../function_tests_break/mitigation_none', 'NWS', True, DROPs, 'max_infected')
    o, k = break_function('mitigation_random', 'NWS', True, DROPs, 'max_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('NWS NONStatic --- Max Infected')
    plt.xlabel('Drops')
    plt.xticks(range(len(m)), DROPs)
    plt.ylabel('Max Infected')
    plt.show()

    # BA NON Static
    m, i = break_function('mitigation_all_F1', 'BA', True, Ms, 'max_infected')
    n, j = break_function('../function_tests_break/mitigation_none', 'BA', True, Ms, 'max_infected')
    o, k = break_function('mitigation_random', 'BA', True, Ms, 'max_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('BA NONStatic --- Max Infected')
    plt.xlabel('M')
    plt.xticks(range(len(m)), Ms)
    plt.ylabel('Max Infected')
    plt.show()

    # PCG NON Static
    m, i = break_function('mitigation_all_F1', 'PCG', True, N_EDGESs, 'max_infected')
    n, j = break_function('mitigation_none', 'PCG', True, N_EDGESs, 'max_infected')
    o, k = break_function('mitigation_random', 'PCG', True, N_EDGESs, 'max_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    # PCG new stuff
    m, i = break_function('mitigation_PCG_F1', 'PCG', True, N_EDGESs, 'max_infected')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F2', 'PCG', True, N_EDGESs, 'max_infected')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F2')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F3', 'PCG', True, N_EDGESs, 'max_infected')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F3')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    # End PCG New Stuff


    plt.legend()
    plt.title('PCG NONStatic --- Max Infected')
    plt.xlabel('N_Edges')
    plt.xticks(range(len(m)), N_EDGESs)
    plt.ylabel('Max Infected')
    plt.show()

    #################################
    ## Total Infected ##

    # ER NON Static
    m, i = break_function('mitigation_all_F1', 'ER', True, EDGE_ps, 'total_infected')
    n, j = break_function('../function_tests_break/mitigation_none', 'ER', True, EDGE_ps, 'total_infected')
    o, k = break_function('mitigation_random', 'ER', True, EDGE_ps, 'total_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('ER NONStatic --- Total Infected')
    plt.xlabel('Edge Connection Probabilities')
    plt.xticks(range(len(EDGE_ps)), EDGE_ps)
    plt.ylabel('total_infected')
    plt.show()


    # NWS NON Static
    m, i = break_function('mitigation_all_F1', 'NWS', True, DROPs, 'total_infected')
    n, j = break_function('../function_tests_break/mitigation_none', 'NWS', True, DROPs, 'total_infected')
    o, k = break_function('mitigation_random', 'NWS', True, DROPs, 'total_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('NWS NONStatic --- Total Infected')
    plt.xlabel('Drops')
    plt.xticks(range(len(m)), DROPs)
    plt.ylabel('total_infected')
    plt.show()

    # BA NON Static
    m, i = break_function('mitigation_all_F1', 'BA', True, Ms, 'total_infected')
    n, j = break_function('../function_tests_break/mitigation_none', 'BA', True, Ms, 'total_infected')
    o, k = break_function('mitigation_random', 'BA', True, Ms, 'total_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('BA NONStatic --- Total Infected')
    plt.xlabel('M')
    plt.xticks(range(len(m)), Ms)
    plt.ylabel('total_infected')
    plt.show()

    # PCG NON Static
    m, i = break_function('mitigation_all_F1', 'PCG', True, N_EDGESs, 'total_infected')
    n, j = break_function('mitigation_none', 'PCG', True, N_EDGESs, 'total_infected')
    o, k = break_function('mitigation_random', 'PCG', True, N_EDGESs, 'total_infected')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    # PCG new stuff
    m, i = break_function('mitigation_PCG_F1', 'PCG', True, N_EDGESs, 'total_infected')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F2', 'PCG', True, N_EDGESs, 'total_infected')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F2')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F3', 'PCG', True, N_EDGESs, 'total_infected')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F3')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    # End PCG New Stuff

    plt.legend()
    plt.title('PCG NONStatic --- Total Infected')
    plt.xlabel('N Edges')
    plt.xticks(range(len(m)), N_EDGESs)
    plt.ylabel('total_infected')
    plt.show()

    ################
    ## Mitigations Used ##

    # ER NON Static
    m, i = break_function('mitigation_all_F1', 'ER', True, EDGE_ps, 'mitigation')
    n, j = break_function('../function_tests_break/mitigation_none', 'ER', True, EDGE_ps, 'mitigation')
    o, k = break_function('mitigation_random', 'ER', True, EDGE_ps, 'mitigation')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('ER NONStatic --- Mitigation Used')
    plt.xlabel('Edge Connection Probabilities')
    plt.xticks(range(len(EDGE_ps)), EDGE_ps)
    plt.ylabel('Mitigations Used')
    plt.show()


    # NWS NON Static
    m, i = break_function('mitigation_all_F1', 'NWS', True, DROPs, 'mitigation')
    n, j = break_function('../function_tests_break/mitigation_none', 'NWS', True, DROPs, 'mitigation')
    o, k = break_function('mitigation_random', 'NWS', True, DROPs, 'mitigation')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('NWS NONStatic --- Mitigation Used')
    plt.xlabel('Drops')
    plt.xticks(range(len(m)), DROPs)
    plt.ylabel('Mitigation Used')
    plt.show()

    # BA NON Static
    m, i = break_function('mitigation_all_F1', 'BA', True, Ms, 'mitigation')
    n, j = break_function('../function_tests_break/mitigation_none', 'BA', True, Ms, 'mitigation')
    o, k = break_function('mitigation_random', 'BA', True, Ms, 'mitigation')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    plt.legend()
    plt.title('BA NONStatic --- Mitigation Used')
    plt.xlabel('M')
    plt.xticks(range(len(m)), Ms)
    plt.ylabel('Mitigation Used')
    plt.show()

    # PCG NON Static
    m, i = break_function('mitigation_all_F1', 'PCG', True, N_EDGESs, 'mitigation')
    n, j = break_function('mitigation_none', 'PCG', True, N_EDGESs, 'mitigation')
    o, k = break_function('mitigation_random', 'PCG', True, N_EDGESs, 'mitigation')
    m = np.array(m)
    n = np.array(n)
    o = np.array(o)
    i = np.array(i)
    j = np.array(j)
    k = np.array(k)

    plt.plot(m, label='F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    plt.plot(n, label='None')
    plt.fill_between(range(len(n)), (n-j), (n+j), alpha=0.1)
    plt.plot(o, label='Random')
    plt.fill_between(range(len(o)), (o-k), (o+k), alpha=0.1)

    # PCG new stuff
    m, i = break_function('mitigation_PCG_F1', 'PCG', True, N_EDGESs, 'mitigation')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F1')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F2', 'PCG', True, N_EDGESs, 'mitigation')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F2')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 

    m, i = break_function('mitigation_PCG_F3', 'PCG', True, N_EDGESs, 'mitigation')
    m = np.array(m)
    i = np.array(i)
    plt.plot(m, label='PCG-F3')
    plt.fill_between(range(len(m)), (m-i), (m+i), alpha=0.1) 
    # End PCG New Stuff

    plt.legend()
    plt.title('PCG NONStatic --- Mitigation Used')
    plt.xlabel('N Edges')
    plt.xticks(range(len(m)), N_EDGESs)
    plt.ylabel('Mitigation Used')
    plt.show()

# Load Results

# Use for simple
#RESULTS_DIRECTORY = "./function_tests/"
# Use for the use all/secondary strategy
RESULTS_DIRECTORY = "./function_tests_use_all/"
#RESULTS_DIRECTORY = "./function_tests_break/"
#RESULTS_DIRECTORY = "./function_tests_use_all_break/"
#RESULTS_DIRECTORY = "./function_tests_grow/"
#RESULTS_DIRECTORY = "./function_tests_use_all_grow/"


model = snetwork.setup_network(0,0,0,0, size=500, edge_p=0.04)

measure_keys = ['susceptible', 
        'max_infected', 
        'total_infected', 
        #'removed',            
        'removed_p',
        'mitigation', 
        'mitigation_effective', 
        'mitigation_ineffective']

# For ER graph
EDGE_ps = [0.015, 0.016, 0.017, 0.018, 0.019, 0.020, 0.021, 0.022, 0.023, 0.024, 0.025, 0.026, 0.027, 0.028, 0.029, 0.030, 0.031, 0.032, 0.033, 0.034, 0.035, 0.036, 0.037, 0.038, 0.039, 0.040, 0.041, 0.042, 0.043, 0.044, 0.045]

# For NWS graph
DROPs = [1100, 1000, 875, 750, 625, 500, 375, 250, 125, 0]
# for BA graph
Ms = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
# For PCG
N_EDGESs = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]


GRAPH_SIZEs = [500, 1000, 1500, 2000]


#print('break')
#do_break()
#print('grow')
#do_grow()


print(generate_summary_statistic_table(FUNCTIONS_NONSTATIC_PCG, model, measure_keys))
#print()

#print(generate_summary_statistic_table(FUNCTIONS_DYNAMIC, model, measure_keys))
#print()

#print(generate_p_val_table(FUNCTIONS_STATIC, FUNCTIONS_DYNAMIC, model, measure_keys))
#print()


#d20 = load_data('mitigation_degree20_True')
#f1 = load_data('mitigation_F1_True')
#f3 = load_data('mitigation_F3_True')
#f5 = load_data('mitigation_F5_True')

#a = get_average_trends(*get_all_trends(f1, model))
#average_epidemic_plot(a, 'Trends: F1')

#generate_p_val_matrix(FUNCTIONS_DYNAMIC, ['Degree 20', 'F1', 'F3', 'F5'], [4, 6, 8, 10], 'Susceptible', 'susceptible', model)
#generate_p_val_matrix(FUNCTIONS_DYNAMIC, ['Degree 20', 'F1', 'F3', 'F5'], [4, 6, 8, 10], 'Max Infected', 'max_infected', model)
#generate_p_val_matrix(FUNCTIONS_DYNAMIC, ['Degree 20', 'F1', 'F3', 'F5'], [4, 6, 8, 10], 'Total Infected', 'total_infected', model)
#generate_p_val_matrix(FUNCTIONS_DYNAMIC, ['Degree 20', 'F1', 'F3', 'F5'], [4, 6, 8, 10], 'Mitigations', 'mitigation', model)

'''
f1_m = get_single_measures(load_data(FUNCTIONS_DYNAMIC[6]), model)
f3_m = get_single_measures(load_data(FUNCTIONS_DYNAMIC[8]), model)
f5_m = get_single_measures(load_data(FUNCTIONS_DYNAMIC[10]), model)

compare_distros(f3_m['total_infected'], f1_m['total_infected'], 'F3', 'F1', "Total Infected")
compare_distros(f3_m['total_infected'], f5_m['total_infected'], 'F3', 'F5', "Total Infected")

compare_distros(f3_m['mitigation'], f1_m['mitigation'], 'F3', 'F1', "Total Mitigations")
compare_distros(f3_m['mitigation'], f5_m['mitigation'], 'F3', 'F5', "Total Mitigations")
'''
