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

fig = plt.figure(figsize=(cm2inch(4.), cm2inch(3.)))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(top=0.95,bottom=0.1,left=0.12,right=1.,hspace=0.1,wspace=0.1)
ax1 = plt.subplot(gs1[0,0])

data = pd.read_csv("calcium_data_wo-metal-disc.csv")
data =data.dropna()
data["normed_firing_rate"] = data["firing_rate"]/np.mean(data[data["timing"]=="pre"]["firing_rate"].values)
# plot boxplot
sns.barplot(data=data,x="timing",y="normed_firing_rate",order=["pre","1st"],palette=["#293241ff","#98c1d9ff"],capsize=0.1,ax=ax1)


### add stats ###
ax1.text(1,0.8,"***",fontsize=12,ha='center',va='bottom')

for ax in [ax1]:
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.yaxis.set_ticks_position('left')
	ax.xaxis.set_ticks_position('bottom')

	ax.set_xlim(-1,2)
	ax.set_ylim(0,1.2)
	ax.set_xticks([0,1])
	ax.set_xlabel("")

ax1.set_xticklabels(["in petri dish","in chamber"])
ax1.set_ylabel(r"$\mathrm{\bf{normalized\ [Ca^{2+}]_i\ spikes}}$")
ax1.set_xlabel("")

plt.savefig("calcium.svg")

plt.show()