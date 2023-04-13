#loading file
import pickle
import pandas as pd 
import matplotlib.pyplot as plt

res_name = 'dcEF-calcium-CA1_diff_mask_std3'
with open(res_name, 'rb') as f:
    results = pickle.load(f)

#With this file, you can have a quick overview of the masks used for each culture for extraction 

def plot_mask(temp_var_color,neuron_dict_filtered):
    fig, ax = plt.subplots()
    fig.set_size_inches(12,12)
    ax.imshow(temp_var_color)

    for neuron in neuron_dict_filtered.keys():
        neuron_hull = neuron_dict_filtered[neuron]
        ax.annotate(str(neuron),xy = (neuron_hull[1][0],neuron_hull[0][0]),
                                color='white',
                                fontsize=12,
                                weight = 'bold',
                                horizontalalignment='center',
                                verticalalignment='center')


for experiment in results.keys():
    for prep_date in results[experiment].keys():
        for culture in results[experiment][prep_date].keys():
            for recording in results[experiment][prep_date][culture].keys():
                temp_var_color = results[experiment][prep_date][culture][recording]['mask_color']
                neuron_dict_filtered = results[experiment][prep_date][culture][recording]['neuron_dictionary_filtered']

                plot_mask(temp_var_color,neuron_dict_filtered)
                plt.title(str(experiment)+" "+str(prep_date)+" "+str(culture)+" "+str(recording))
                plt.savefig("./masks/"+str(experiment)+" "+str(prep_date)+" "+str(culture)+" "+str(recording)+".png")





