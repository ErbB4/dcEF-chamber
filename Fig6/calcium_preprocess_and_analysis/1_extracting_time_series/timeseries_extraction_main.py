"""
Created by shreyash garg

Python script to extract time series data from confocal microscopy based imaging
The algorithm identifies neurons using morphological openings and closing and having
size above a given pixel area/threshold

This example python file works for batch processing multiple files.
To work on single file use timeseries_extraction_example.py

Input: Raw data for all experiments

Output: python dictionary containing time series data of identified neurons
"""

"""
Import libraries
"""
import czifile
import numpy as np
from lxml import etree
import pickle
import cv2 as cv2
import os
from skimage.measure import label

# specify the path containing all the data
mainpath = 'G:/dcEF-calcium-CA1/data'

# initialise dictionary holding the results
results = {}

# iterate over all experiment types
for experiment in next(os.walk(mainpath))[1]:
    print(experiment)
    results[experiment] = {}
    current_dir = mainpath + '/' + experiment

    # iterate over preparation days
    for prep_date in next(os.walk(current_dir))[1]:
        current_dir_prepdate = current_dir + '/' + prep_date
        results[experiment][prep_date] = {}

        # iterate over cell cultures
        for culture in next(os.walk(current_dir_prepdate))[1]:
            results[experiment][prep_date][culture] = {}
            print(culture)
            foldername = current_dir_prepdate + '/' + culture
            print(foldername)

            for file in os.listdir(foldername):
                filename = os.fsdecode(file)

                # exclude image files
                if filename.startswith("image"):
                    continue
                else:

                    """
                    read data from czi file and store it in a numpy array
                    """
                    try:
                        raw_image = czifile.imread(foldername + '/' + filename)
                    except OSError:
                        print("Could not open/read file:")
                        continue


                    results[experiment][prep_date][culture][filename] = {}

                    """
                    extract info from the czi image's metadata
                    """
                    czi = czifile.CziFile(foldername + '/' + filename)

                    czi = czifile.CziFile(foldername + '/'+filename)
                    czi_xml_str = czi.metadata()

                    # create element tree of metadata
                    czi_parsed = etree.fromstring(czi_xml_str)

                    # date and time of imaging
                    creation_date = (czi_parsed.xpath("//CreationDate")[0]).text

                    # size of image (in pixels)
                    x_dim = int((czi_parsed.xpath("//SizeX")[0]).text)
                    y_dim = int((czi_parsed.xpath("//SizeY")[0]).text)

                    # physical dimension of pixel (in meters)
                    x_resolution = float((czi_parsed.xpath('//Items//Value')[0]).text)
                    y_resolution = float((czi_parsed.xpath('//Items//Value')[1]).text)

                    # name of the channel i.e., tdtomato, egfp
                    channel0_name = (czi_parsed.xpath('//Channels//Name')[0]).text
                    channel1_name = (czi_parsed.xpath('//Channels//Name')[2]).text

                    # time resolution of imaging
                    time_res = float((czi_parsed.xpath('//LaserScanInfo//FrameTime')[0]).text)

                    # total number of frames in the recording
                    frames = int((czi_parsed.xpath('//SizeT')[0]).text)

                    # overall time of recording
                    total_time = frames * time_res

                    raw_image_squeezed = np.squeeze(raw_image)
                    """
                    data pre processing
                    """
                    # remove useless dimensions from the numpy array
                    raw_image_squeezed = np.squeeze(raw_image)

                    # extracting data for both channels and store separately
                    channel0 = raw_image_squeezed[:, 0, :, :]
                    channel1 = raw_image_squeezed[:, 1, :, :]

                    """
                    neuron contour identification from tdtomato recording
                    """

                    # select how long to average the recording. first select the type
                    # if averaging = full, then average over whole recording
                    # if averaging = user_defined then average for first few defined seconds

                    averaging = 'full'

                    # averaging = 'user_defined'
                    # averaging_time = 30 # in seconds

                    # create a slice of first few frames which would be used for cell contour detection
                    # channel1 is tdtomato

                    if averaging == 'full':
                        tomato_slice = channel1[:frames, :, :]
                    elif averaging == 'user_defined':
                        frames_averaged = int(averaging_time / time_res)
                        tomato_slice = channel1[:frames_averaged, :, :]

                    # average over the slice
                    tomato_slice_mean = np.mean(tomato_slice, 0)

                    """
                    Image processing
                    """
                    # convert it to float 32 otherwise medianblur would give error
                    tomato_slice_mean = np.float32(tomato_slice_mean)

                    # remove noise using medianblur
                    # specify kernel size for noise removal
                    noise_kern_size = 5
                    tomato_slice_lownoise = cv2.medianBlur(tomato_slice_mean, noise_kern_size)

                    # perform morphological opening
                    # initialise kernel for first opening
                    kernel_1 = np.ones((32, 32), np.uint8)

                    # perform opening
                    tomato_slice_lownoise_open1 = cv2.morphologyEx(tomato_slice_lownoise, cv2.MORPH_OPEN, kernel_1)

                    # first remove the background from averaged image
                    background_removed = tomato_slice_mean - tomato_slice_lownoise_open1

                    # initialise kernel for second opening and then open
                    kernel_2 = np.ones((2, 2), np.uint8)

                    # perform second opening
                    opened_image = cv2.morphologyEx(background_removed, cv2.MORPH_OPEN, kernel_2)

                    # """
                    # The boundaries are still not going away so we try to implement erosion
                    # """
                    #
                    # #perform erosion
                    # #opened_image = cv2.erode(opened_image,kernel_2,iterations = 1)
                    #

                    # binarise image using thresholding. The threshold value was determined by looking at raw recording in image viewer
                    threshold_val = 100
                    max_val = 1

                    ret, tomato_cleaned = cv2.threshold(opened_image, threshold_val, max_val, cv2.THRESH_BINARY)

                    """
                    Neuron identification by identifying connected regions in binarised image
                    """

                    # find the label for each connected region
                    label_im = label(tomato_cleaned)

                    # extract all the labels for identified regions
                    label_unique = np.unique(label_im)

                    # create a dictionary to store all identified regions
                    neuron_dict = {}
                    for ind in label_unique:
                        # exclude index 0 as it is just the background
                        if ind != 0:
                            # get coordinates of all the pixels belonging to given component
                            neuron_dict[ind] = np.where(label_im == ind)

                    # temporary array to visualise contour of all neurons having size about a given threshold
                    mask = np.zeros(tomato_cleaned.shape)

                    # create separate dictionary which contains data only for putative neurons
                    # contains neuronwise data for only those who have size bigger than 20
                    neuron_dict_filtered = {}
                    for key in neuron_dict.keys():
                        if np.size(neuron_dict[key]) > 20:
                            neuron_dict_filtered[key] = neuron_dict[key]
                            # make all pixels 1 if we consider given component as putative neuron
                            mask[neuron_dict[key]] = 1

                    results[experiment][prep_date][culture][filename]['mask'] = mask

                    """
                    This section is used to generate mask images with neuron number 
                    """
                    mask_color = np.zeros((tomato_cleaned.shape[0], tomato_cleaned.shape[1], 3), dtype='int32')
                    for r in range(tomato_cleaned.shape[0]):
                        for c in range(tomato_cleaned.shape[1]):
                            if mask[r, c] == 1:
                                mask_color[r, c, 0] = 255

                    results[experiment][prep_date][culture][filename]['mask_color'] = mask_color
                    results[experiment][prep_date][culture][filename]['neuron_dictionary_filtered'] = neuron_dict_filtered

                    """
                     alternate way to store timeseries would be to store in a dictionary and pickle dump.
                     I thought of using numpy array but then the data is not too big
                    and its easier to keep track of neuron ID in dictionary
                    """
                    comp_timeseries_dict = {}

                    for neuron in neuron_dict_filtered.keys():
                        # save timeseries data averaged over all pixels
                        comp_timeseries_dict[neuron] = np.mean(
                            channel0[:, neuron_dict_filtered[neuron][0], neuron_dict_filtered[neuron][1]], axis=1)

                    results[experiment][prep_date][culture][filename]['time_series'] = comp_timeseries_dict


res_name = 'dcEF-calcium-CA1_diff_mask_std3'
with open(res_name, 'wb') as f:
    pickle.dump(results, f)
