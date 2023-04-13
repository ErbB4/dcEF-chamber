#loading file
import pickle
import pandas as pd 
import numpy as np 

res_name = 'dcEF-calcium-CA1_diff_mask_std3'
with open(res_name, 'rb') as f:
    results = pickle.load(f)


def gather_data_for_each_experiment(experiment):
    data = []
    for prep_date in results[experiment].keys():
        for culture in results[experiment][prep_date].keys():
            for recording in results[experiment][prep_date][culture].keys():
                for neuron in results[experiment][prep_date][culture][recording]["time_series_processed"].keys():
                    neuron_data = results[experiment][prep_date][culture][recording]["time_series_processed"][neuron]
                    data.append(
                        {
                         "experiment": experiment,
                         "prep_date": prep_date,
                         "culture": culture,
                         "recording": recording,
                         "neuron": neuron,
                         "firing_rate": neuron_data["firing_rate"][0]
                        }
                        )
                    

    df = pd.DataFrame(data)
    df["timing"] = df["recording"].str.slice(0,3)
    df["group"] = df["culture"].str[-4::]
    df["culture_ID"] = df["culture"].str.slice(0,-5)
    df.pop("culture")
    df.pop("recording")

    df.to_csv("calcium_data_"+experiment+".csv")

#gather for wo/metal-disc
gather_data_for_each_experiment('wo-metal-disc')
gather_data_for_each_experiment('with-metal-disc')
gather_data_for_each_experiment('100x-DC')
gather_data_for_each_experiment('100x-pulse-2Hz')
