'''
Author:     James Hughes
Date:       June 12, 2020

Version:    0.3


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
MEASURE_EVERY = 7
FUNCTIONS_STATIC = [
            'mitigation_none_False', 
            'mitigation_random_False',
            'mitigation_traveler_False',
            #'mitigation_degree5_False', 
            #'mitigation_degree10_False', 
            'mitigation_degree15_False',
            'mitigation_degree20_False',
            'mitigation_degree25_False', 
            'mitigation_F1_False',
            'mitigation_F2_False',
            'mitigation_F3_False',
            'mitigation_F4_False',
            'mitigation_F5_False',
            ]       # CHANGE ME FOR SWITCHING OUT FUNCTIONS

FUNCTIONS_DYNAMIC = [
            'mitigation_none_True', 
            'mitigation_random_True',
            'mitigation_traveler_True',
            #'mitigation_degree5_True', 
            #'mitigation_degree10_True', 
            'mitigation_degree15_True',
            'mitigation_degree20_True', 
            'mitigation_degree25_True', 
            'mitigation_F1_True',
            'mitigation_F2_True',
            'mitigation_F3_True',
            'mitigation_F4_True',
            'mitigation_F5_True',
            ]       # CHANGE ME FOR SWITCHING OUT FUNCTIONS

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
    average_trends[0] = []
    average_trends[1] = []
    average_trends[2] = []
    average_trends[3] = []
    average_trends['3_p'] = []
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

    # 3_PRIME
    # Since we only have 1 mitigate count for every mitigation_period, we need to count carefully
    for i in range(len(average_trends[3])):
        if(i < mitigate_period):
            average_trends['3_p'].append(average_trends[3][i])
        else:
            average_trends['3_p'].append(average_trends[3][i] - average_trends['effective'][(i - mitigate_period)//mitigate_period])

    # Make the 3' an array
    average_trends['3_p'] = np.array(average_trends['3_p'])
    return average_trends

# Generate average epidemic curve plot
def average_epidemic_plot(results, fName, mitigate_period=7):

    plt.bar(range(mitigate_period, len(results[0]), mitigate_period), results['total'], width=mitigate_period, align='edge', color='m', alpha=0.2, label='Total Mitigations')
    plt.bar(range(mitigate_period, len(results[0]), mitigate_period), results['effective'], width=mitigate_period, align='edge', color='m', alpha=0.4, label='Effective Mitigations')
    plt.bar(np.arange(mitigate_period, len(results[0]), mitigate_period), results['ineffective'], width=mitigate_period, align='edge', color='m', alpha=0.6, label='Ineffective Mitigations')
    plt.plot(results[0], color='b', label='Susceptible')
    plt.plot(results[1], color='g', label='Exposed')
    plt.plot(results[2], color='y', label='Infected')
    plt.plot(results[3], color='r', label='Removed')
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





# Load Results

model = snetwork.setup_network(0,0,0,0, size=500, edge_p=0.04)

measure_keys = ['susceptible', 
        'max_infected', 
        'total_infected', 
        #'removed',            
        'removed_p',
        'mitigation', 
        'mitigation_effective', 
        'mitigation_ineffective']

#print(generate_summary_statistic_table(FUNCTIONS_STATIC, model, measure_keys))
#print()

#print(generate_summary_statistic_table(FUNCTIONS_DYNAMIC, model, measure_keys))
#print()

#print(generate_p_val_table(FUNCTIONS_STATIC, FUNCTIONS_DYNAMIC, model, measure_keys))
#print()


d20 = load_data('mitigation_degree20_True')
f1 = load_data('mitigation_F1_True')
f3 = load_data('mitigation_F3_True')
f5 = load_data('mitigation_F5_True')

#a = get_average_trends(*get_all_trends(f5, model))
#average_epidemic_plot(a, 'Trends: F5')

#generate_p_val_matrix(FUNCTIONS_DYNAMIC, ['Degree 20', 'F1', 'F3', 'F5'], [4, 6, 8, 10], 'Susceptible', 'susceptible', model)
#generate_p_val_matrix(FUNCTIONS_DYNAMIC, ['Degree 20', 'F1', 'F3', 'F5'], [4, 6, 8, 10], 'Max Infected', 'max_infected', model)
#generate_p_val_matrix(FUNCTIONS_DYNAMIC, ['Degree 20', 'F1', 'F3', 'F5'], [4, 6, 8, 10], 'Total Infected', 'total_infected', model)
#generate_p_val_matrix(FUNCTIONS_DYNAMIC, ['Degree 20', 'F1', 'F3', 'F5'], [4, 6, 8, 10], 'Mitigations', 'mitigation', model)

f1_m = get_single_measures(load_data(FUNCTIONS_DYNAMIC[6]), model)
f3_m = get_single_measures(load_data(FUNCTIONS_DYNAMIC[8]), model)
f5_m = get_single_measures(load_data(FUNCTIONS_DYNAMIC[10]), model)

compare_distros(f3_m['total_infected'], f1_m['total_infected'], 'F3', 'F1', "Total Infected")
compare_distros(f3_m['total_infected'], f5_m['total_infected'], 'F3', 'F5', "Total Infected")

compare_distros(f3_m['mitigation'], f1_m['mitigation'], 'F3', 'F1', "Total Mitigations")
compare_distros(f3_m['mitigation'], f5_m['mitigation'], 'F3', 'F5', "Total Mitigations")
