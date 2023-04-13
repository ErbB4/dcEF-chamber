#loading file
import pickle
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

res_name = 'dcEF-calcium-CA1_diff_mask_std3'
with open(res_name, 'rb') as f:
    results = pickle.load(f)


def plot_mask(temp_var_color,neuron_dict_filtered,ax):
    ax.imshow(temp_var_color,cmap='plasma')
    for neuron in [1,20,30,40,50,60]:
        neuron_hull = neuron_dict_filtered[neuron]
        ax.annotate(str(neuron),xy = (neuron_hull[1][0],neuron_hull[0][0]),
                                    color='white',
                                    fontsize=6,
                                    horizontalalignment='center',
                                    verticalalignment='center')


plt.rcParams["axes.titlesize"]=10
plt.rcParams["axes.labelsize"]=8
plt.rcParams["lines.linewidth"]=0.5
plt.rcParams["lines.markersize"]=5
plt.rcParams["xtick.labelsize"]=6
plt.rcParams["ytick.labelsize"]=6
plt.rcParams["legend.fontsize"]=6

plt.rcParams.update({'font.family':'arial'})
plt.rcParams['mathtext.fontset'] = 'dejavusans'

def cm2inch(value):
    return value/2.54


fig = plt.figure(figsize=(cm2inch(4), cm2inch(4)))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(top=1.,bottom=0.0,left=0.0,right=1.,hspace=0.0,wspace=0.0)
ax1 = plt.subplot(gs1[0,0])

temp_var_color = results["wo-metal-disc"]["16-08-2022"]["2-1-2-sham"]["2nd.czi"]['mask_color']
neuron_dict_filtered = results["wo-metal-disc"]["16-08-2022"]["2-1-2-sham"]["2nd.czi"]['neuron_dictionary_filtered']

plot_mask(temp_var_color,neuron_dict_filtered,ax1)
ax1.axis("off")
plt.savefig("mask.svg")





