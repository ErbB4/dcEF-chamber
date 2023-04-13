import numpy as np 
import scipy as sp 
import matplotlib.pyplot as plt 
import pandas as pd 
import matplotlib.gridspec as gridspec
import seaborn as sns 
from scipy import stats

####figure settings####
plt.rcParams["axes.titlesize"]=10
plt.rcParams["axes.labelsize"]=8
plt.rcParams["axes.linewidth"]=.5
plt.rcParams["lines.linewidth"]=.5
plt.rcParams["lines.markersize"]=2
plt.rcParams["xtick.labelsize"]=6
plt.rcParams["ytick.labelsize"]=6
plt.rcParams["font.family"] = "arial"
plt.rcParams['mathtext.fontset'] = 'dejavusans'
plt.rcParams["legend.fontsize"] = 6
plt.rcParams['xtick.minor.width'] = 0.5
plt.rcParams['xtick.major.width'] = 0.5
plt.rcParams['ytick.minor.width'] = 0.5
plt.rcParams['ytick.major.width'] = 0.5


def cm2inch(value):
    return value/2.54
#######################

fig = plt.figure(figsize=(cm2inch(8.5), cm2inch(3.)))
gs1 = gridspec.GridSpec(1, 2)
gs1.update(top=0.95,bottom=0.1,left=0.12,right=.9,hspace=0.1,wspace=0.1)
ax1 = plt.subplot(gs1[0,0])
ax2 = plt.subplot(gs1[0,1])

data1 = pd.read_csv("calcium_data_strong_pulse_2Hz.csv")
data1 = data1.dropna()
data_sham = data1[data1["group"]=="sham"]
data_stim = data1[data1["group"]=="stim"]

data_sham["normed_firing_rate"] = data_sham["firing_rate"]/np.mean(data_sham[data_sham["timing"]=="pre"]["firing_rate"].values)
data_stim["normed_firing_rate"] = data_stim["firing_rate"]/np.mean(data_stim[data_stim["timing"]=="pre"]["firing_rate"].values)

# plot boxplot
sns.barplot(data=data_stim,x="timing",y="normed_firing_rate",order=["pre","dur"],palette=["w","#3d5a80ff"],edgecolor=['k','none'],capsize=0.1,linewidth=0.5,ax=ax1)
sns.barplot(data=data_sham,x="timing",y="normed_firing_rate",order=["pre","dur"],palette=["w","#98c1d9ff"],edgecolor=['k','none'],capsize=0.1,linewidth=0.5,ax=ax2)


### add stats ###
# stats were performed and uniformally documented in the lab using GraphPad 
ax1.text(1,1.7,"***",fontsize=12,ha='center',va='bottom')
ax2.text(1,1.1,"ns",fontsize=8,ha='center',va='bottom')

for ax in [ax1,ax2]:
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.yaxis.set_ticks_position('left')
	ax.xaxis.set_ticks_position('bottom')

	ax.set_xlim(-1,2)
	ax.set_ylim(0,2.)
	ax.set_xticks([0,1])
	ax.set_xlabel("")

ax1.set_xticklabels(["baseline","pulsed dcEF"])
ax2.set_xticklabels(["baseline","sham"])

ax1.set_ylabel(r"$\mathrm{\bf{normalized\ [Ca^{2+}]_i\ spikes}}$")
ax2.set_ylabel("")
ax2.set_yticks([])

plt.savefig("calcium_strong_pulse.svg")

plt.show()