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

def stats(data):
    naive = data[data["group"]=="na"]["IntDen"].values
    sham  = data[data["group"]=="sham"]["IntDen"].values
    high  = data[data["group"]=="high"]["IntDen"].values

    t = sp.stats.kruskal(naive,sham,high)[1]
    a = sp.stats.mannwhitneyu(naive,sham)[1]
    b = sp.stats.mannwhitneyu(naive,high)[1]
    c = sp.stats.mannwhitneyu(sham,high)[1]

    print(len(naive))
    print(len(sham))
    print(len(high))
    
    print(t)
    print(a)
    print(b)
    print(c)

    return t,a,b,c

def plot_scatter(data,ax,colors):
    sns.boxplot(data=data,x="group",y="IntDen",order=["na","sham","high"],color='w',showfliers = False,saturation=1.,ax=ax)
    plt.setp(ax.artists, edgecolor = 'k', facecolor='w')
    plt.setp(ax.lines, color='k')
    sns.swarmplot(data=data,x="group", y="IntDen", size=4.,order=["na","sham","high"],palette=colors,ax=ax)

fig = plt.figure(figsize=(cm2inch(4.), cm2inch(5)))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(top=0.95,bottom=0.1,left=0.22,right=0.99,hspace=0.1,wspace=0.1)
ax1 = plt.subplot(gs1[0,0])
colors = ['#293241','#98c1d9','#3d5a80']

data = pd.read_csv("cFos_data.csv")
data =data.dropna()
ax1.axhline(y=1,linestyle='--',color='k',linewidth=0.5)

plot_scatter(data,ax1,colors)

### add stats ###
t,a,b,c = stats(data)
print(t)
print(a)
print(b)
print(c)

if t<0.001:
    pass

if c>0.05:
    ax1.plot([1,2],[2.1,2.1],"k-")
    ax1.text(1.5,2.13,"ns",fontsize=8,ha='center',va="bottom")

ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.yaxis.set_ticks_position('left')
ax1.xaxis.set_ticks_position('bottom')
ax1.text(3.,1.01,"baseline",va='bottom',ha='right',fontsize=6)

ax1.set_xlim(-1,3)
ax1.set_xticks([0,1,2])
ax1.set_xticklabels(["naïve","chamber","dcEF"])
ax1.set_ylabel(r"$\mathrm{\bf{normalized\ c{-}Fos\ intensity}}$")
ax1.set_xlabel("")

plt.savefig("c-Fos.svg")

plt.show()