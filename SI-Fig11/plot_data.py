import numpy as np 
import matplotlib.pyplot as plt 
from pathlib import Path 
import matplotlib.gridspec as gridspec
import scipy as sp
from scipy import stats
import pandas as pd 
import seaborn as sns


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


def plot_lines(data,ax):
    pre  = data[data["sequence"]=="pre"]["IntDen"].values
    post = data[data["sequence"]=="post"]["IntDen"].values

    for i in np.arange(0,6,1):
        ax.plot([0,1],[pre[i],post[i]],'-',color='k',alpha=0.2)

    ax.text(1,15.4,"ns",fontsize=10,ha='center',va='center')


def plot_scatter(data,ax,colors):
    sns.boxplot(data=data,x="sequence",y="IntDen",order=["pre","post"],color='w',showfliers = False,saturation=1.,ax=ax)
    plt.setp(ax.artists, edgecolor = 'k', facecolor='w')
    plt.setp(ax.lines, color='k')
    sns.swarmplot(data=data,x="sequence", y="IntDen", size=4.,order=["pre","post"],palette=colors,ax=ax)


def stats(data):
    pre  = data[data["sequence"]=="pre"]["IntDen"].values
    post = data[data["sequence"]=="post"]["IntDen"].values

    a = sp.stats.wilcoxon(pre,post)[1]
    return a


############## plot TNF intensity ##############
fig = plt.figure(figsize=(cm2inch(5), cm2inch(4.4)))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(top=0.97,bottom=0.12,left=0.22,right=0.99,hspace=0.1,wspace=0.1)
ax1 = plt.subplot(gs1[0,0])

colors = ['#3d5a80','#ee6c4d']

data = pd.read_csv("data_merged.csv")
plot_scatter(data,ax1,colors)
plot_lines(data,ax1)

a= stats(data)
print(a)

ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.yaxis.set_ticks_position('left')
ax1.xaxis.set_ticks_position('bottom')

ax1.set_ylabel(r"$\mathrm{\bf{eGFP\ intensity}}$ | a.u.")
ax1.set_xlim(0.5,2.5)
ax1.set_xticks([0,1])
ax1.set_xticklabels(["baseline","after treatment"])

ax1.set_xlim(-1,2)
ax1.set_xlabel("")
plt.savefig("TNF-magnet.svg")


plt.show()