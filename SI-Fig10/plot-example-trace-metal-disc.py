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

fig = plt.figure(figsize=(cm2inch(5.5), cm2inch(3.5)))
gs1 = gridspec.GridSpec(4, 1)
gs1.update(top=1.,bottom=0.0,left=0.0,right=1.,hspace=0.0,wspace=0.0)
ax1 = plt.subplot(gs1[0,0])
ax2 = plt.subplot(gs1[1,0])
ax3 = plt.subplot(gs1[2,0])
ax4 = plt.subplot(gs1[3,0])


plot_example("wo-metal-disc","26-01-2023","5-1-1-sham","pre.czi",43,"#293241",ax1)
plot_example("with-metal-disc","27-01-2023","3-1-1-stim","1st.czi",6,"#ffbb96ff",ax2)
plot_example("with-metal-disc","27-01-2023","3-1-1-stim","2nd.czi",13,"#3d5a80",ax3)
plot_example("with-metal-disc","30-01-2023","7-1-2-sham","2nd.czi",3,"#98c1d9",ax4)


for ax in [ax1,ax2,ax3,ax4]:
    ax.axis("off")
plt.savefig("example.svg")
plt.show()


