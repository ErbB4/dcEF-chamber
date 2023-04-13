#loading file
import pickle
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp  
from scipy import signal

res_name = 'dcEF-calcium-CA1_diff_mask_std3'
with open(res_name, 'rb') as f:
    results = pickle.load(f)

# different combinations of preprocessing was defined here

def detrend_trace(intensity):
	#only detrend the raw trace
    data = pd.DataFrame({"RawIntDen": intensity})
    rolling_window = 20
    data["RawIntDen_median"] = data["RawIntDen"].rolling(rolling_window).median()
    data["RawIntDen_trend"] = data["RawIntDen_median"].fillna(
        data.RawIntDen_median.iloc[rolling_window-1]
    )
    data["RawIntDen_detrend"] = data.RawIntDen - data.RawIntDen_trend
    return data["RawIntDen_detrend"].values


def rescale_and_detrend_trace(intensity):
	#detrend and rescale the trace
    data = pd.DataFrame({"RawIntDen": intensity})
    rolling_window = 20
    data["RawIntDen_median"] = data["RawIntDen"].rolling(rolling_window).median()
    data["RawIntDen_trend"] = data["RawIntDen_median"].fillna(
        data.RawIntDen_median.iloc[rolling_window-1]
    )
    data["RawIntDen_detrend"] = data.RawIntDen - data.RawIntDen_trend
    data["RawIntDen_rescaled"] = data.RawIntDen_detrend/np.mean(data.RawIntDen_trend)
    return data["RawIntDen_rescaled"].values


def moving_smoothing(intensity_series):
	#moving average the trace with a small window size 2
    data = pd.DataFrame({"Intensity": intensity_series})
    rolling_window = 2
    data["Intensity_mean"] = data["Intensity"].rolling(rolling_window).mean()
    data["Intensity_smoothed"] = data["Intensity_mean"].fillna(
        data.Intensity_mean.iloc[rolling_window-1]
    )
    return data["Intensity_smoothed"].values


def get_trace_stats(intensity_series,threshold_ratio=3):
	#this function was defined to detect spikes for trace after different proprocessing
    data = pd.DataFrame({"Intensity": intensity_series})
    data["reference"] = (
        data.Intensity.mean() + threshold_ratio * data.Intensity.std()
    )
    data["is_above_threshold"] = (data.Intensity >= data.reference).astype(int)
    data = data.reset_index().rename(columns={"index": "time_order"})
    data["is_above_threshold_change"] = data.is_above_threshold.diff()
    spike_boundary_index = data.loc[
        data.is_above_threshold_change != 0
    ].dropna().time_order
    data["time"] = data.time_order/len(data)*120
    firing_rate = int(len(spike_boundary_index) / 2) / 120
    return int(len(spike_boundary_index) / 2) #spike numbers

def analyze_trace(raw_intensity,type,threshold_ratio=3):
	#get the spike numbers under different preprocessing method
    if type == "raw":
        spike_n = get_trace_stats(raw_intensity,threshold_ratio=3)
    if type == "detrend":
        detrended_intensity = detrend_trace(raw_intensity)
        spike_n = get_trace_stats(detrended_intensity,threshold_ratio=3)
    if type == "detrend_smooth":
        detrended_intensity = detrend_trace(raw_intensity)
        smoothed_intensity = moving_smoothing(detrended_intensity)
        spike_n = get_trace_stats(smoothed_intensity,threshold_ratio=3)
    if type == "rescale_detrend":
        rescaled_intensity = rescale_and_detrend_trace(raw_intensity)
        spike_n = get_trace_stats(rescaled_intensity,threshold_ratio=3)
    if type == "rescale_detrend_smooth":
        rescaled_intensity = rescale_and_detrend_trace(raw_intensity)
        smoothed_intensity = moving_smoothing(rescaled_intensity)
        spike_n = get_trace_stats(smoothed_intensity,threshold_ratio=3)
    return spike_n

def plot_individual_trace(experiment):
	#plot individual trace for each neuron in each culture and annotate the spike numbers with different methods
	#for quality control reason
	#this function takes forever to finish, for quick check please use the function below
    for experiment in [experiment]:
        for prep_date in results[experiment].keys():
            for culture in results[experiment][prep_date].keys():
                for recording in results[experiment][prep_date][culture].keys():
                    for neuron in results[experiment][prep_date][culture][recording]["time_series_processed"].keys():
                        plt.figure(figsize=(6,4))
                        neuron_data = results[experiment][prep_date][culture][recording]["time_series_processed"][neuron]
                        raw = neuron_data["RawIntDen"].values
                        detrend = detrend_trace(raw)
                        smoothed = moving_smoothing(detrend)
                        processed_1 = rescale_and_detrend_trace(raw)
                        processed_2 = moving_smoothing(rescale_and_detrend_trace(raw))
                        
                        plt.subplot(2,1,1)
                        #plot detrend data, old method
                        spike_n = get_trace_stats(detrend,3.)
                        plt.plot(np.linspace(0,120,len(detrend)),detrend,color='blue', label='detrended data')
                        plt.axhline(y=np.mean(detrend)+3.*np.std(detrend),linestyle='--',color='blue')
                        plt.text(0,40,str(spike_n)+" spikes",fontsize=16,color='blue')

                        #plot smoothed detrended data
                        spike_n = get_trace_stats(smoothed,3.)
                        plt.plot(np.linspace(0,120,len(smoothed)),smoothed,color='grey', label='smoothed detrended data')
                        plt.axhline(y=np.mean(smoothed)+3.*np.std(smoothed),linestyle='--',color='grey')
                        plt.text(60,40,str(spike_n)+" spikes",fontsize=16,color='grey')
                        plt.ylim(-50,50)

                        #plot processed data (re-scaled, detrended, with/or/without being filtered)
                        plt.subplot(2,1,2)
                        spike_n = get_trace_stats(processed_1,3.)
                        plt.plot(np.linspace(0,120,len(processed_1)),processed_1,color='k',label="double")
                        plt.axhline(y=np.mean(processed_1)+3.*np.std(processed_1),linestyle='--',color='k')
                        plt.text(0,0.5,str(spike_n)+" spikes",fontsize=16,color='k')

                        spike_n = get_trace_stats(processed_2,3)
                        plt.plot(np.linspace(0,120,len(processed_2)),processed_2,color='r',label="triple")
                        plt.axhline(y=np.mean(processed_2)+3.*np.std(processed_2),linestyle='--',color='r')
                        plt.text(60,0.5,str(spike_n)+" spikes",fontsize=16,color='r')
                        plt.ylim(-1,1)


                        plt.savefig("./traces/"+str(experiment)+"/"+str(prep_date)+"/"+str(culture)+"/"+str(recording)[0:-4]+"/"+str(neuron)+".png")
                print(str(experiment)+" "+str(prep_date)+" "+str(culture)+" finished plotting!")



def quick_test_function():
	#instead of plotting all the traces, a quick test function is implemented here for you to compare different preprosessing methods.
    
    neuron_data = results["wo-metal-disc"]["25-07-2022"]["4-2-sham"]["pre.czi"]["time_series_processed"][36]
    raw_intensity = neuron_data["RawIntDen"].values

    plt.figure()
    plt.plot(np.linspace(1,120,len(raw_intensity)),raw_intensity,color='red')

    detrended = detrend_trace(raw_intensity)
    FR = get_trace_stats(detrended)
    plt.plot(np.linspace(1,120,len(detrended)),detrended,color='blue')
    plt.axhline(y=np.mean(detrended)+3*np.std(detrended),linewidth=0.5,linestyle='--',color='blue')
    plt.text(0,np.mean(detrended)+2*np.std(detrended),str(FR)+ " spikes",color='blue')

    smoothed = moving_smoothing(detrended)
    FR = get_trace_stats(smoothed,3.)
    plt.plot(np.linspace(1,120,len(smoothed)),smoothed,color='grey')
    plt.axhline(y=np.mean(smoothed)+3.*np.std(smoothed),linewidth=0.5,linestyle='--',color='grey')
    plt.text(80,np.mean(smoothed)+2*np.std(smoothed),str(FR)+ " spikes",color='grey')


    plt.show()


########## call function to check the methods and individual traces ##############
#quick check
test_function()
#thorough check
get_FR_with_different_methods("wo-metal-disc")

# afterwards you can decide which method to apply in the final dataset