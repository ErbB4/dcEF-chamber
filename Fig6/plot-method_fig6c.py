import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

#loading file
import pickle
res_name = 'dcEF-calcium-CA1_diff_mask_std3'
with open(res_name, 'rb') as f:
    results = pickle.load(f)


def rescale_and_detrend_trace(intensity):
    data = pd.DataFrame({"RawIntDen": intensity})
    rolling_window = 20
    data["RawIntDen_median"] = data["RawIntDen"].rolling(rolling_window).median()
    data["RawIntDen_trend"] = data["RawIntDen_median"].fillna(
        data.RawIntDen_median.iloc[rolling_window-1]
    )
    data["RawIntDen_detrend"] = data.RawIntDen - data.RawIntDen_trend
    data["RawIntDen_rescaled"] = data.RawIntDen_detrend/np.mean(data.RawIntDen_trend)
    return data["RawIntDen_rescaled"].values, data["RawIntDen_trend"].values

def plot_example(experiment,prep,culture,timing,neuron_id,color,ax):
    neuron_data = results[experiment][prep][culture][timing]["time_series_processed"][neuron_id]
    cdata = neuron_data["RawIntDen"].values
    x = np.linspace(0,120,len(cdata))
    data_new = rescale_and_detrend_trace(cdata)[0]
    ax.plot(x,data_new,linestyle='-',color=color)
    ax.axhline(y=np.mean(data_new)+3*np.std(data_new),linestyle='--',color='#2d6a4f')

def plot_process(experiment,prep,culture,timing,neuron_id,ax1,ax2):
    neuron_data = results[experiment][prep][culture][timing]["time_series_processed"][neuron_id]
    cdata = neuron_data["RawIntDen"].values
    x = np.linspace(0,120,len(cdata))
    data_new,trend = rescale_and_detrend_trace(cdata)
    ax1.plot(x,cdata,linestyle='-',color='#6c757d',label='raw trace')
    ax1.plot(x,trend,linestyle='--',color='#e07a5f',label='trend')
    ax2.plot(x,data_new,linestyle='-',color='#293241',label='processed')
    ax1.axhline(y=np.mean(cdata)+3*np.std(cdata),linestyle='--',color='#2d6a4f')
    ax2.axhline(y=np.mean(data_new)+3*np.std(data_new),linestyle='--',color='#2d6a4f',label='threshold: mean+3SD')
    ax1.legend(bbox_to_anchor=(0, 1.1, 0.95, 0.2), loc=1,ncol=2, mode="expand", borderaxespad=0.,frameon=False,fontsize=6)
    ax2.legend(bbox_to_anchor=(0, 1.1, 0.95, 0.2), loc=1,ncol=2, mode="expand", borderaxespad=0.,frameon=False,fontsize=6)

plt.rcParams["axes.titlesize"]=10
plt.rcParams["axes.labelsize"]=8
plt.rcParams["lines.linewidth"]=0.5
plt.rcParams["lines.markersize"]=5
plt.rcParams["xtick.labelsize"]=6
plt.rcParams["ytick.labelsize"]=6
plt.rcParams["legend.fontsize"]=6

plt.rcParams.update({'font.family':'arial'})
plt.rcParams['mathtext.fontset'] = 'dejavusans'


def cm2inch(value):
    return value/2.54


fig = plt.figure(figsize=(cm2inch(5.5), cm2inch(6)))
gs1 = gridspec.GridSpec(5, 1)
gs1.update(top=.8,bottom=0.0,left=0.0,right=1.,hspace=0.0,wspace=0.0)
ax1 = plt.subplot(gs1[0,0])
ax2 = plt.subplot(gs1[1,0])
ax3 = plt.subplot(gs1[3,0])
ax4 = plt.subplot(gs1[4,0])


plot_process("wo-metal-disc","25-07-2022","4-2-sham","pre.czi",1,ax1,ax2)
plot_example("wo-metal-disc","25-07-2022","4-2-sham","pre.czi",36,'#293241',ax3)
plot_example("wo-metal-disc","25-07-2022","4-2-sham","pre.czi",37,'#293241',ax4)

for ax in [ax1,ax2,ax3,ax4]:
    ax.axis("off")
#ax1.set_ylim(-500,3200)
plt.savefig("method-trace.svg")
plt.show()


