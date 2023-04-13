
"""
Python script used to generate mask images with neuron number
"""

import matplotlib.pyplot as plt
import numpy as np

def masks_plotter(tomato_cleaned, temp_var, neuron_dict_filtered, filename):
    temp_var_color = np.zeros((tomato_cleaned.shape[0],tomato_cleaned.shape[1],3),dtype = 'int32')
    for r in range(tomato_cleaned.shape[0]):
        for c in range(tomato_cleaned.shape[1]):
            if temp_var[r,c]== 1:
                temp_var_color[r,c,0] = 255

    #the following lines which are commented generate black and white image
    # fig, ax = plt.subplots()
    # fig.set_size_inches(12,12)
    # imshow(temp_var)
    # for neuron in neuron_dict_filtered.keys():
    #     neuron_hull = neuron_dict_filtered[neuron]
    #     ax.annotate(str(neuron),xy = (neuron_hull[1][0],neuron_hull[0][0]), color='white',
    #                 fontsize=12,weight = 'bold',
    #                 horizontalalignment='center',
    #                 verticalalignment='center')


    #following lines plot color image with neuron ID
    fig, ax = plt.subplots()
    fig.set_size_inches(12,12)
    ax.imshow(temp_var_color)
    ax.set_title('Masks obtained from tdtomato with neuron IDs (neurons were filtered based on size)')
    for neuron in neuron_dict_filtered.keys():
        neuron_hull = neuron_dict_filtered[neuron]
        ax.annotate(str(neuron),xy = (neuron_hull[1][0],neuron_hull[0][0]), color='white',
                    fontsize=12,weight = 'bold',
                    horizontalalignment='center',
                    verticalalignment='center')
    plt.savefig(filename + '_mask.png')