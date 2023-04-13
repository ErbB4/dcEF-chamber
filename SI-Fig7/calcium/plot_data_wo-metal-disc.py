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

fig = plt.figure(figsize=(cm2inch(8), cm2inch(5.)))
gs1 = gridspec.GridSpec(1, 2)
gs1.update(top=0.95,bottom=0.1,left=0.12,right=1.,hspace=0.1,wspace=0.1)
ax2 = plt.subplot(gs1[0,0])
ax3 = plt.subplot(gs1[0,1])

data = pd.read_csv("calcium_data_wo-metal-disc.csv")
data =data.dropna()
data_sham = data[data["group"]=="sham"]
data_stim = data[data["group"]=="stim"]
data_sham["normed_firing_rate"] = data_sham["firing_rate"]/np.mean(data_sham[data_sham["timing"]=="1st"]["firing_rate"].values)
data_stim["normed_firing_rate"] = data_stim["firing_rate"]/np.mean(data_stim[data_stim["timing"]=="1st"]["firing_rate"].values)

# plot boxplot
sns.barplot(data=data_stim,x="timing",y="normed_firing_rate",order=["1st","2nd"],palette=["#ffbb96ff","#3d5a80ff"],capsize=0.1,ax=ax2)
sns.barplot(data=data_sham,x="timing",y="normed_firing_rate",order=["1st","2nd"],palette=["#ffbb96ff","#98c1d9ff"],capsize=0.1,ax=ax3)


### add stats ###
# stats were performed and uniformally documented in the lab using GraphPad 

ax2.text(1,1.6,"***",fontsize=12,ha='center',va='bottom')
ax3.text(1,1.6,"***",fontsize=12,ha='center',va='bottom')

for ax in [ax2,ax3]:
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.yaxis.set_ticks_position('left')
	ax.xaxis.set_ticks_position('bottom')

	ax.set_xlim(-1,2)
	ax.set_ylim(0,2.)
	ax.set_xticks([0,1])
	ax.set_xlabel("")

ax2.set_xticklabels(["in petri dish","in chamber"])
ax2.set_xticklabels(["1st","2nd (dcEF)"])
ax3.set_xticklabels(["1st","2nd (sham)"])
ax2.set_title("dcEF")
ax3.set_title("sham")

ax3.set_ylabel("")
ax3.set_yticks([])

ax2.set_ylabel(r"$\mathrm{\bf{normalized\ [Ca^{2+}]_i\ spikes}}$")
ax2.set_xlabel("")

plt.savefig("calcium-supp.svg")

plt.show()