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

def stats(data):
    dcEF = data[data["group"]=="dcEF"]["IntDen"].values
    magnet = data[data["group"]=="magnet"]["IntDen"].values

    a = sp.stats.mannwhitneyu(dcEF,magnet)[1]
    return a

def plot_scatter(data,ax,colors):
    sns.boxplot(data=data,x="group",y="IntDen",order=["dcEF","magnet"],color='w',showfliers = False,saturation=1.,ax=ax)
    plt.setp(ax.artists, edgecolor = 'k', facecolor='w')
    plt.setp(ax.lines, color='k')
    sns.swarmplot(data=data,x="group", y="IntDen", size=4.,order=["dcEF","magnet"],palette=colors,ax=ax)


fig = plt.figure(figsize=(cm2inch(3.8), cm2inch(2.5)))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(top=0.9,bottom=0.15,left=0.32,right=0.99,hspace=0.1,wspace=0.1)
ax1 = plt.subplot(gs1[0,0])
colors = ['#3d5a80','#83c5be']

data = pd.read_csv("merged_data.csv")
data =data.dropna()
plot_scatter(data,ax1,colors)

### add stats ###
a = stats(data)
print(a)

if a>0.05:
    ax1.text(1,0.8,"ns",fontsize=8,ha='center',va="bottom")


ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.yaxis.set_ticks_position('left')
ax1.xaxis.set_ticks_position('bottom')
ax1.set_xlim(-0.5,1.5)
ax1.set_xticks([0,1])
ax1.set_xticklabels(["w/o","w/ metal disk"])
ax1.set_ylabel(r"$\mathrm{\bf{c{-}Fos\ intensity}}$ | a.u.")
ax1.set_xlabel("")
ax1.set_ylim(0.,1)
plt.savefig("c-Fos-magnet.eps")

plt.show()