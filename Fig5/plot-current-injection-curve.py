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


fig = plt.figure(figsize=(cm2inch(5), cm2inch(4.)))
gs1 = gridspec.GridSpec(4, 1)
gs1.update(top=0.95,bottom=0.05,left=0.05,right=.9,hspace=0.1,wspace=0.1)
ax1 = plt.subplot(gs1[0,0])
ax2 = plt.subplot(gs1[1,0])
ax3 = plt.subplot(gs1[2,0])
ax4 = plt.subplot(gs1[3,0])


def plot_trace_centered(trace,ax,label):
	trace.setSweep(sweepNumber=60,channel=2)
	amps = trace.sweepY# - np.median(trace.sweepY)
	Is = np.arange(-100,501,10)
	colors = ['#293241','#98c1d9','#3d5a80']
	if label == 'control':
		color = colors[0]
	if label == 'chamber_only':
		color = colors[1]
	if label == 'dcEF':
		color = colors[2]
	if label == 'chamber_control':
		color = colors[1]

	ax.plot(trace.sweepX*1000,amps,color=color,label=label)
	ax.set_title(str(label), color=color,fontsize=6)
	ax.set_xlim(-10,np.array(trace.sweepX*1000)[-1]+100)



T = "./control/"
trace = pyabf.ABF(T+"2022_07_25_0006.abf")
plot_trace_centered(trace,ax1,"control")

T = "./Chamber/"
trace = pyabf.ABF(T+"2022_07_25_0042.abf")
plot_trace_centered(trace,ax2,"chamber_only")

T = "./Chamber/"
trace = pyabf.ABF(T+"2023_01_26_0049.abf")
plot_trace_centered(trace,ax3,"chamber_control")

T = "./Chamber_stim/"
trace = pyabf.ABF(T+"2023_01_26_0016.abf")
plot_trace_centered(trace,ax4,"dcEF")



for ax in [ax1,ax2,ax3,ax4]:
	ax.spines['left'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)

	ax.set_xticks([])
	ax.set_yticks([])

ax1.plot([1500,2000],[-50,-50],'k-',linewidth=1.)
ax1.plot([2000,2000],[-50,-25],'k-',linewidth=1.)

plt.savefig("trace-IV.svg")

plt.show()