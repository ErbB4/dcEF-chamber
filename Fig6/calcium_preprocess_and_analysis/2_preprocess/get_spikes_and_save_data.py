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
    return int(len(spike_boundary_index) / 2), firing_rate #spike numbers and FR

def analyze_trace(raw_intensity,type,threshold_ratio=3):
	#get the spike numbers or FR under different preprocessing method
    if type == "raw":
        spike_n = get_trace_stats(raw_intensity,threshold_ratio=3)[0]
    if type == "detrend":
        detrended_intensity = detrend_trace(raw_intensity)
        spike_n = get_trace_stats(detrended_intensity,threshold_ratio=3)[0]
    if type == "detrend_smooth":
        detrended_intensity = detrend_trace(raw_intensity)
        smoothed_intensity = moving_smoothing(detrended_intensity)
        spike_n = get_trace_stats(smoothed_intensity,threshold_ratio=3)[0]
    if type == "rescale_detrend":
        rescaled_intensity = rescale_and_detrend_trace(raw_intensity)
        spike_n = get_trace_stats(rescaled_intensity,threshold_ratio=3)[0]
    if type == "rescale_detrend_smooth":
        rescaled_intensity = rescale_and_detrend_trace(raw_intensity)
        smoothed_intensity = moving_smoothing(rescaled_intensity)
        spike_n = get_trace_stats(smoothed_intensity,threshold_ratio=3)[0]
    return spike_n



########## call function to get the final dataset ##############
# this step comes after the quality contorl of individual traces.
# after you decide which method to apply in the final dataset, use this function to gee the final dataset
def get_FR_with_different_methods(experiment):
    data = []
    for prep_date in results[experiment].keys():
        for culture in results[experiment][prep_date].keys():
            for recording in results[experiment][prep_date][culture].keys():
                for neuron in results[experiment][prep_date][culture][recording]["time_series_processed"].keys():
                    neuron_data = results[experiment][prep_date][culture][recording]["time_series_processed"][neuron]
                    raw_intensity = neuron_data["RawIntDen"].values

                    data.append(
                        {
                         "experiment": experiment,
                         "prep_date": prep_date,
                         "culture": culture,
                         "recording": recording,
                         "neuron": neuron,
                         "firing_rate": analyze_trace(raw_intensity,"rescale_detrend_smooth",3.) # we used rescale_detrend_smooth
                        }
                        )

    df = pd.DataFrame(data)
    df["timing"] = df["recording"].str.slice(0,3)
    df["group"] = df["culture"].str[-4::]
    df["culture_ID"] = df["culture"].str.slice(0,-5)
    df.pop("culture")
    df.pop("recording")

    df.to_csv("calcium_data_"+experiment+".csv")