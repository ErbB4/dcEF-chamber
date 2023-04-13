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
plt.rcParams["lines.linewidth"]=1.
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


def plot_scatter(data,ax,colors):
    sns.boxplot(data=data,x="Label_group",y="normed",order=["naive-control","chamber-only","with-stimulation","positive-control"],color='w',showfliers = False,saturation=1.,ax=ax)
    plt.setp(ax.artists, edgecolor = 'k', facecolor='w')
    plt.setp(ax.lines, color='k')
    sns.swarmplot(data=data,x="Label_group", y="normed", size=4.,order=["naive-control","chamber-only","with-stimulation","positive-control"],palette=colors,ax=ax)


####plotting####
fig = plt.figure(figsize=(cm2inch(4.2), cm2inch(4.5)))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(top=0.97,bottom=0.12,left=0.22,right=0.99,hspace=0.1,wspace=0.1)
ax1 = plt.subplot(gs1[0,0])
colors = ['#293241','#98c1d9','#3d5a80','#ee6c4d']

data = pd.read_csv("data_merged.csv")
data =data.dropna()
plot_scatter(data,ax1,colors)

####add stats####
#For uniform documentation reason, statistical analysis was performed in GraphPad and stored in the lab server. So we only use the results here.

ax1.plot([0.,3.],[3.6,3.6],'k-',linewidth=0.5)
ax1.plot([0.,0.],[3.,3.6],'k-',linewidth=0.5)
ax1.plot([3.,3.],[3.5,3.6],'k-',linewidth=0.5)

ax1.plot([0.,1.],[1.8,1.8],'k-',linewidth=0.5)
ax1.plot([0.,0.],[1.7,1.8],'k-',linewidth=0.5)
ax1.plot([1.,1.],[1.7,1.8],'k-',linewidth=0.5)

ax1.plot([0.,2.],[2.2,2.2],'k-',linewidth=0.5)
ax1.plot([0.,0.],[2.0,2.2],'k-',linewidth=0.5)
ax1.plot([2.,2.],[2.0,2.2],'k-',linewidth=0.5)

ax1.text(1.5,3.52,"*",fontsize=12,ha='center',va='bottom')
ax1.text(0.5,1.82,"ns",fontsize=8,ha='center',va='bottom')
ax1.text(1.,2.22,"ns",fontsize=8,ha='center',va='bottom')

####modify axes####
ax1.axhline(y=1,linestyle='--',color='k',linewidth=0.5)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.yaxis.set_ticks_position('left')
ax1.xaxis.set_ticks_position('bottom')
ax1.text(3.5,1.01,"baseline",va='bottom',ha='right',fontsize=6)
ax1.set_xlim(-0.5,3.5)
ax1.set_xticks([0,1,2,3])
ax1.set_xticklabels(["naïve","chamber","dcEF","NMDA"])
ax1.set_ylabel(r"$\mathrm{\bf{normalized\ SG\ intensity}}$")
ax1.set_xlabel("")

plt.savefig("SG-stats.svg")

####display####
plt.show()
