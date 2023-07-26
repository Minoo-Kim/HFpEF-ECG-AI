#!/usr/bin/env python
# coding: utf-8

# In[20]:


import wfdb
import numpy as np
import matplotlib.pyplot as plt
import biosppy
import scipy.signal as signal
import time
import os


# In[21]:


# general useful functions
def print_ecg(record_path):
    signal, fields = wfdb.rdsamp(record_path)

    # Extract necessary information from fields
    signal_names = fields['sig_name']
    fs = fields['fs']
    units = fields['units']

    # Create a time axis for x-axis plotting
    num_samples = len(signals)
    duration = num_samples / fs
    time = list(range(num_samples))  # Convert range object to a list
    time = [t / fs for t in time]  # Divide each element by the sampling frequency

    # Plot each signal
    for i in range(len(signal_names)):
        plt.plot(time, signals[:, i], label=signal_names[i])
        plt.xlabel('Time (s)')
        plt.ylabel(f'{signal_names[i]} ({units[i]})')
        plt.title('ECG Waveform')
        plt.grid(True)
        plt.legend()
        plt.show()


# In[22]:


# preposess ECGS
def remove_baseline_wander(record_path):
   # Read the ECG record using wfdb.rdsamp
    signals, fields = wfdb.rdsamp(record_path)

   # Apply high-pass filter to remove baseline wander
    filtered_signals = signal.butter(4, 0.5, fs=fields['fs'], btype='highpass', output='sos')
    baseline_removed = signal.sosfilt(filtered_signals, signals, axis=0)
    
    # temporarily combining median_filter
    # Adjust the window size to fit within the signal length
    window_size = 3

    # Apply median filter to remove noise
    baseline_removed = signal.medfilt(baseline_removed, kernel_size=window_size)
    
    
    
    # Plotting code
    num_samples = baseline_removed.shape[0]
    time = range(num_samples)

    # Plot each lead of the baseline-corrected ECG signals
    num_leads = baseline_removed.shape[1]
    for lead in range(num_leads):
        plt.plot(time, baseline_removed[:, lead], label=fields['sig_name'][lead])
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('ECG Signals with Baseline Wander Removed (High-pass Filter)')
        plt.legend()
        plt.grid(True)
        plt.show()


# In[23]:


def median_filter(record_path):
    # Read the ECG record using wfdb.rdsamp
    signals, fields = wfdb.rdsamp(record_path)
    
    # Adjust the window size to fit within the signal length
    window_size = 3

    # Apply median filter to remove noise
    filtered_signals = signal.medfilt(signals, kernel_size=window_size)

    # Create a time axis for x-axis plotting
    num_samples = filtered_signals.shape[0]
    time = range(num_samples)

    # Plot each lead of the filtered ECG signals
 #   num_leads = filtered_signals.shape[1]
  #  for lead in range(num_leads):
  #      plt.plot(time, filtered_signals[:, lead], label=fields['sig_name'][lead])
  #      plt.xlabel('Time')
 #       plt.ylabel('Amplitude')
  #      plt.title('12-Lead ECG Signals after Noise Removal (Median Filter)')
 #       plt.legend()
 #       plt.grid(True)
  #      plt.show()


# In[24]:


# below are functions to calculate each ECG feature

# for amplitude
def calculate_amplitude(ecg):
    ecg = np.array(ecg)
    return np.max(ecg) - np.min(ecg)

def rpeaks_indices(ecg):
    return biosppy.signals.ecg.christov_segmenter(ecg)[0]

def calc_p_angle(ecg):
    # Extract P-wave segments around R-peaks
    p_wave_segments = []
    rpeak_indices = rpeaks_indices(ecg[:,0])
    freq = 1000
    for rpeak_index in rpeak_indices:
        start_index = max(0, rpeak_index - int(0.1 * freq))
        end_index = min(len(ecg[:,0]), rpeak_index + int(0.2 * freq))
        p_wave_segment = ecg[start_index:end_index, 0]
        print(p_wave_segment)
        p_wave_segments.append(p_wave_segment)

    # Concatenate P-wave segments into a single array
    p_wave_segments = np.concatenate(p_wave_segments)

    # Calculate the mean P-wave segment
    mean_p_wave_segment = np.mean(p_wave_segments)
    print(mean_p_wave_segment)

    # Calculate the P-wave angle
    p_wave_angle = np.arctan2(mean_p_wave_segment[1], mean_p_wave_segment[0]) * 180 / np.pi


# In[26]:


# Extract the ECG signal and metadata
# graph ECG for demo
start = time.time()
record_path = "/Users/minookim/Desktop/LCICM/ecg_extraction/mimic-iv-ecg/files/p10000032/s100780919/100780919"
print_ecg(record_path)
end = time.time()
print(end-start)


# In[18]:


# preprocess ECGs; uncomment accordingly
# remove_baseline_wander(record_path)

# calculate median_filtering times
# most basic caae
start = time.time()
median_filter(record_path)
end = time.time()
print(end-start) # 0.018616199493408203 seconds for 1

# every file in the 12-lead ECG subset
# totals to 659 files
def absoluteFilePaths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))
directory = "/Users/minookim/Desktop/LCICM/ecg_extraction/mimic-iv-ecg/files/"

# ecg_filepaths now contains every ecg_filepath in the subset
ecg_filepaths = list(absoluteFilePaths(directory))
ecg_filepaths = [val for val in ecg_filepaths if val.endswith(".dat")]
ecg_filepaths = [val[:-4] for val in ecg_filepaths]
start = time.time()
for record in ecg_filepaths:
    median_filter(record)
end = time.time()
print(end-start) # 3.952536106109619 seconds for 659


# In[19]:


# calculate amplitudes
amps = []
for i in range(12):
    amps.append(calculate_amplitude(ecgs[0][:, i]))
    
print(amps)


# In[ ]:


# calculate p_wave_angles

print(calc_p_angle(ecgs[0]))


# In[ ]:


# test r peak
print(rpeaks_indices(ecgs[0][:, i]))


# In[ ]:





# In[ ]:




