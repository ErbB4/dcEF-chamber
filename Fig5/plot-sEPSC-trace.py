#This plotting script was not used for Fig5.
#But for documentation reason we store it here to showcase how to use pyabf package to plot trace and change trace colors.

import numpy as np 
import pyabf
import matplotlib.pyplot as plt 
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


fig = plt.figure(figsize=(cm2inch(5.5), cm2inch(4.)))
gs1 = gridspec.GridSpec(3, 1)
gs1.update(top=0.95,bottom=0.05,left=0.05,right=.95,hspace=0.1,wspace=0.1)
ax1 = plt.subplot(gs1[0,0])
ax2 = plt.subplot(gs1[1,0])
ax3 = plt.subplot(gs1[2,0])

def plot_trace_centered(trace,starting_time,ax,color,label):
	amps = trace.sweepY - np.median(trace.sweepY)
	ax.plot(trace.sweepX*1000,amps,color=color,label=label)
	ax.set_ylim(-70,30)
	ax.set_xlim(starting_time,starting_time+2000.)


T = "./control/"
trace = pyabf.ABF(T+"2022_07_25_0003.abf")
trace.setSweep(sweepNumber=0,channel=2)
plot_trace_centered(trace,89000.,ax1,"#293241","control")

T = "./Chamber/"
trace = pyabf.ABF(T+"2022_07_25_0043.abf")
trace.setSweep(sweepNumber=0,channel=2)
plot_trace_centered(trace,76280.,ax2,"#98c1d9","chamber")

T = "./Chamber_stim/"
trace = pyabf.ABF(T+"2023_01_26_0019.abf")
trace.setSweep(sweepNumber=0,channel=2)
plot_trace_centered(trace,74000.,ax3,"#3d5a80","dcEF")

ax3.plot([75000,75500],[-50,-50],'k-',linewidth=1.)
ax3.plot([75500,75500],[-50,0],'k-',linewidth=1.)


for ax in [ax1,ax2,ax3]:
	ax.spines['left'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)

	ax.set_xticks([])
	ax.set_yticks([])


plt.savefig("trace.svg")

plt.show()