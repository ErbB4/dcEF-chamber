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


fig = plt.figure(figsize=(cm2inch(4), cm2inch(4.)))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(top=0.95,bottom=0.05,left=0.05,right=.95,hspace=0.1,wspace=0.1)
ax1 = plt.subplot(gs1[0,0])

def plot_trace_centered(trace,starting_time,ax,color,label):
	amps = trace.sweepY - np.median(trace.sweepY)
	ax.plot(trace.sweepX*1000,amps,color=color,label=label)
	ax.set_ylim(-75,15)
	ax.set_xlim(starting_time,starting_time+50.)


T = "./control/"
trace = pyabf.ABF(T+"2022_07_25_0003.abf")
trace.setSweep(sweepNumber=0,channel=2)
plot_trace_centered(trace,89410.,ax1,"#293241","control")

ax1.plot([89420,89440],[-50,-50],'k-',linewidth=1.)
ax1.plot([89420,89420],[-50,-25],'k-',linewidth=1.)


for ax in [ax1]:
	ax.spines['left'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)

	ax.set_xticks([])
	ax.set_yticks([])


plt.savefig("trace-event.svg")

plt.show()